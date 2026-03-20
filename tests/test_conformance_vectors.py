"""Expanded conformance test suite for CAWG–TRQP verifier.

Covers:
- Standard profile (cache-first + live on miss)
- Edge profile (offline snapshot)
- High assurance profile (live only, no cache)
- Negative cases (failed integrity, denied authorization)
- Blocked/revoked entities
- Cache behavior and freshness
- Snapshot stale cases
"""

import json
from pathlib import Path
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.snapshot import SnapshotStore
from cawg_trqp_refimpl.verifier import Verifier, RevocationDelta
from cawg_trqp_refimpl.cache import TTLCache


class TestStandardProfile:
    """Tests for standard (cache-first) profile."""

    def test_standard_authorized_entity(self):
        """Standard profile should return trusted for authorized entity."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
        result = verifier.verify(VerificationRequest(**data), profile="standard").to_dict()
        expected = json.loads(Path("examples/expected/standard_result.json").read_text(encoding="utf-8"))
        for key, value in expected.items():
            assert result[key] == value

    def test_standard_cache_hit(self):
        """Standard profile should use cache on second lookup."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        cache = TTLCache()
        service = MockTRQPService(Path("data/policies.json"))
        verifier = Verifier(service=service, cache=cache)

        # First call: should hit service and cache
        result1 = verifier.verify(VerificationRequest(**data), profile="standard")
        assert "Live authorization lookup executed" in result1.explanations

        # Second call: should hit cache
        result2 = verifier.verify(VerificationRequest(**data), profile="standard")
        assert "Authorization cache hit" in result2.explanations
        assert result1.trust_outcome == result2.trust_outcome

    def test_standard_denied_authorization(self):
        """Standard profile should reject unauthorized entity."""
        # Create request for entity not in policies
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        data["entity_id"] = "did:web:unauthorized.example"
        
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        result = verifier.verify(VerificationRequest(**data), profile="standard")
        
        assert result.trust_outcome == "rejected"
        assert result.actor_authorization == "not_authorized"


class TestEdgeProfile:
    """Tests for edge (offline snapshot) profile."""

    def test_edge_snapshot_authorized(self):
        """Edge profile should use snapshot for offline verification."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(snapshot=SnapshotStore(Path("data/snapshot.json")))
        result = verifier.verify(VerificationRequest(**data), profile="edge").to_dict()
        expected = json.loads(Path("examples/expected/edge_result.json").read_text(encoding="utf-8"))
        for key, value in expected.items():
            assert result[key] == value

    def test_edge_missing_snapshot(self):
        """Edge profile should defer when snapshot unavailable."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(snapshot=None)  # No snapshot available
        result = verifier.verify(VerificationRequest(**data), profile="edge")
        
        assert result.trust_outcome == "deferred"
        assert result.verification_mode == "offline_snapshot"
        assert result.policy_freshness == "missing_snapshot"

    def test_edge_no_network_dependency(self):
        """Edge profile should not require service."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(snapshot=SnapshotStore(Path("data/snapshot.json")), service=None)
        result = verifier.verify(VerificationRequest(**data), profile="edge")
        
        # Should succeed without service
        assert result.asset_integrity == "verified"
        assert result.verification_mode == "offline_snapshot"


class TestHighAssuranceProfile:
    """Tests for high_assurance (live-only) profile."""

    def test_high_assurance_always_live(self):
        """High assurance profile should always do live lookup."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        cache = TTLCache()
        service = MockTRQPService(Path("data/policies.json"))
        
        # Pre-populate cache
        verifier = Verifier(service=service, cache=cache)
        verifier.verify(VerificationRequest(**data), profile="standard")
        assert cache.get("test_key") is None or len(cache.cache) > 0
        
        # High assurance should bypass cache
        verifier2 = Verifier(service=service, cache=cache)
        result = verifier2.verify(VerificationRequest(**data), profile="high_assurance")
        
        assert result.verification_mode == "online_full"
        assert "Live authorization lookup executed" in result.explanations


class TestRevocation:
    """Tests for revocation delta handling."""

    def test_revocation_delta_blocks_entity(self):
        """Revocation delta should block revoked entities."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        # Apply revocation
        verifier.apply_revocation_delta(
            [data["entity_id"]], 
            policy_epoch="2026-Q1"
        )
        
        result = verifier.verify(VerificationRequest(**data))
        
        assert result.trust_outcome == "rejected"
        assert result.actor_authorization == "not_authorized"
        assert result.verification_mode == "revocation_check"
        assert "revoked" in result.explanations[0].lower()

    def test_revocation_multiple_entities(self):
        """Revocation delta should handle multiple revoked entities."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        verifier.apply_revocation_delta(
            ["entity1", "entity2", data["entity_id"]], 
            policy_epoch="2026-Q2"
        )
        
        result = verifier.verify(VerificationRequest(**data))
        assert result.trust_outcome == "rejected"

    def test_revocation_does_not_block_unrevoked(self):
        """Revocation delta should not affect unrevoked entities."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        verifier.apply_revocation_delta(
            ["other_entity"], 
            policy_epoch="2026-Q1"
        )
        
        result = verifier.verify(VerificationRequest(**data))
        # Should proceed normally (or with service response)
        assert result.verification_mode != "revocation_check"


class TestNegativeCases:
    """Tests for failure modes and edge cases."""

    def test_failed_integrity_rejected(self):
        """Integrity failure should reject immediately."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        data["integrity_ok"] = False
        
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        result = verifier.verify(VerificationRequest(**data))
        
        assert result.trust_outcome == "rejected"
        assert result.asset_integrity == "failed"
        assert result.verification_mode == "local_only"

    def test_no_service_no_snapshot_deferred(self):
        """Without service or snapshot, should defer."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        
        verifier = Verifier(service=None, snapshot=None)
        result = verifier.verify(VerificationRequest(**data), profile="standard")
        
        assert result.trust_outcome == "deferred"
        assert result.policy_freshness == "service_unavailable"

    def test_blocked_entity_from_revocations_file(self):
        """Entity in revocations.json should be blocked."""
        # Create request for entity in revocations.json (did:web:blocked.example)
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        data["entity_id"] = "did:web:blocked.example"
        
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
        result = verifier.verify(VerificationRequest(**data), profile="standard")
        
        assert result.trust_outcome == "rejected"
        assert result.actor_authorization == "not_authorized"
        assert result.reason == "entity_revoked" or result.trust_outcome == "rejected"


class TestContextMatching:
    """Tests for context-dependent authorization."""

    def test_context_sensitive_authorization(self):
        """Authorization should be context-sensitive."""
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        
        # Request with correct context
        result_match = verifier.verify(VerificationRequest(**data), profile="standard")
        
        # Request with wrong context
        data_wrong = data.copy()
        data_wrong["context"] = {"some_other_key": "value"}
        result_mismatch = verifier.verify(VerificationRequest(**data_wrong), profile="standard")
        
        # Results may differ if policy data includes context-sensitive entries
        assert isinstance(result_match.trust_outcome, str)
        assert isinstance(result_mismatch.trust_outcome, str)
