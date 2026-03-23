"""Expanded conformance test suite for CAWG–TRQP verifier."""

import json
from datetime import datetime, timezone
from pathlib import Path

from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.snapshot import SnapshotStore
from cawg_trqp_refimpl.verifier import Verifier
from cawg_trqp_refimpl.cache import TTLCache
from cawg_trqp_refimpl.manifest_parser import CAWGManifestParser


class TestStandardProfile:
    def test_standard_authorized_entity(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
        result = verifier.verify(VerificationRequest(**data), profile="standard").to_dict()
        expected = json.loads(Path("examples/expected/standard_result.json").read_text(encoding="utf-8"))
        for key, value in expected.items():
            assert result[key] == value

    def test_standard_cache_hit(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        cache = TTLCache()
        service = MockTRQPService(Path("data/policies.json"))
        verifier = Verifier(service=service, cache=cache)

        result1 = verifier.verify(VerificationRequest(**data), profile="standard")
        assert "Live authorization lookup executed" in result1.explanations

        result2 = verifier.verify(VerificationRequest(**data), profile="standard")
        assert "Authorization cache hit" in result2.explanations
        assert result1.trust_outcome == result2.trust_outcome

    def test_standard_denied_authorization(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        data["entity_id"] = "did:web:unauthorized.example"
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        result = verifier.verify(VerificationRequest(**data), profile="standard")
        assert result.trust_outcome == "rejected"
        assert result.actor_authorization == "not_authorized"


class TestEdgeProfile:
    def test_edge_snapshot_authorized(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(snapshot=SnapshotStore(Path("data/snapshot.json"), Path("data/trust_anchors.json")))
        result = verifier.verify(VerificationRequest(**data), profile="edge").to_dict()
        expected = json.loads(Path("examples/expected/edge_result.json").read_text(encoding="utf-8"))
        for key, value in expected.items():
            assert result[key] == value

    def test_edge_missing_snapshot(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(snapshot=None)
        result = verifier.verify(VerificationRequest(**data), profile="edge")
        assert result.trust_outcome == "deferred"
        assert result.verification_mode == "offline_snapshot"
        assert result.policy_freshness == "missing_snapshot"

    def test_edge_expired_snapshot_rejected(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        snapshot = SnapshotStore(
            Path("data/snapshot.json"),
            Path("data/trust_anchors.json"),
            current_time=datetime(2027, 1, 1, tzinfo=timezone.utc),
        )
        verifier = Verifier(snapshot=snapshot, service=None)
        result = verifier.verify(VerificationRequest(**data), profile="edge")
        assert result.trust_outcome == "rejected"
        assert result.policy_freshness == "expired_snapshot"


class TestHighAssuranceProfile:
    def test_high_assurance_always_live(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        cache = TTLCache()
        service = MockTRQPService(Path("data/policies.json"))
        verifier = Verifier(service=service, cache=cache)
        verifier.verify(VerificationRequest(**data), profile="standard")
        assert len(cache.cache) > 0

        verifier2 = Verifier(service=service, cache=cache)
        result = verifier2.verify(VerificationRequest(**data), profile="high_assurance")
        assert result.verification_mode == "online_full"
        assert "Live authorization lookup executed" in result.explanations


class TestRevocation:
    def test_revocation_delta_blocks_entity(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        verifier.apply_revocation_delta([data["entity_id"]], policy_epoch="2026-Q1")
        result = verifier.verify(VerificationRequest(**data))
        assert result.trust_outcome == "rejected"
        assert result.actor_authorization == "not_authorized"
        assert result.verification_mode == "revocation_check"
        assert "revoked" in result.explanations[0].lower()

    def test_revocation_does_not_block_unrevoked(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        verifier.apply_revocation_delta(["other_entity"], policy_epoch="2026-Q1")
        result = verifier.verify(VerificationRequest(**data))
        assert result.verification_mode != "revocation_check"


class TestNegativeCases:
    def test_failed_integrity_rejected(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        data["integrity_ok"] = False
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        result = verifier.verify(VerificationRequest(**data))
        assert result.trust_outcome == "rejected"
        assert result.asset_integrity == "failed"
        assert result.verification_mode == "local_only"

    def test_no_service_no_snapshot_deferred(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(service=None, snapshot=None)
        result = verifier.verify(VerificationRequest(**data), profile="standard")
        assert result.trust_outcome == "deferred"
        assert result.policy_freshness == "service_unavailable"


class TestManifestParser:
    def test_c2pa_json_manifest_extracts_signals(self):
        signal = CAWGManifestParser.parse_file(Path("examples/fixtures/cawg_manifest_c2pa.json"))
        assert signal.parser_mode == "c2pa_json"
        assert signal.actor_id == "did:web:publisher.example"
        assert signal.issuer_id == "did:web:issuer.example"
        assert signal.action == "publish"
        assert signal.resource == "cawg:news-content"
        assert signal.context["credential_type"] == "vc:creator-identity"
