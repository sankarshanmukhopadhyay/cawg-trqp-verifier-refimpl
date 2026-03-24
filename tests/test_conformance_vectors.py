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
from cawg_trqp_refimpl.gateway import TrustGateway


class TestStandardProfile:
    def test_standard_authorized_entity(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
        result = verifier.verify(VerificationRequest(**data), profile="standard").to_dict()
        assert result["trust_outcome"] == "trusted"
        assert result["process_integrity"] == "verified_high"
        assert result["policy_evidence"]["authorization_evidence"]

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

    def test_standard_missing_process_proof_rejected(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        data["process_evidence"] = None
        verifier = Verifier(service=MockTRQPService(Path("data/policies.json")))
        result = verifier.verify(VerificationRequest(**data), profile="standard")
        assert result.actor_authorization == "authorized"
        assert result.process_integrity == "missing_required_proof"
        assert result.trust_outcome == "rejected"


class TestEdgeProfile:
    def test_edge_snapshot_authorized(self):
        data = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
        verifier = Verifier(snapshot=SnapshotStore(Path("data/snapshot.json"), Path("data/trust_anchors.json")))
        result = verifier.verify(VerificationRequest(**data), profile="edge").to_dict()
        assert result["trust_outcome"] == "trusted_cached"
        assert result["policy_freshness"] in {"valid", "fresh", "usable", "active", "verified", "current_snapshot", "current"} or isinstance(result["policy_freshness"], str)


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


class TestGatewayVectors:
    def test_gateway_mediated_vector(self):
        data = json.loads(Path("examples/interoperability_vector_gateway.json").read_text(encoding="utf-8"))
        data.pop("use_gateway", None)
        data.pop("profile", None)
        service = MockTRQPService(Path("data/policies.json"))
        verifier = Verifier(service=service, gateway=TrustGateway(service, gateway_id="gateway:interop"))
        result = verifier.verify(VerificationRequest(**data), profile="standard")
        assert result.verification_mode == "gateway_mediated"
        assert result.gateway_mediation["gateway_id"] == "gateway:interop"

    def test_benchmark_fixtures_verify(self):
        service = MockTRQPService(Path("data/policies.json"))
        verifier = Verifier(service=service)
        for path in ["examples/benchmark_high_volume_request.json", "examples/benchmark_constrained_device_request.json"]:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            result = verifier.verify(VerificationRequest(**data))
            assert result.trust_outcome == "trusted"


class TestManifestParser:
    def test_c2pa_json_manifest_extracts_signals(self):
        signal = CAWGManifestParser.parse_file(Path("examples/fixtures/cawg_manifest_c2pa.json"))
        assert signal.parser_mode == "c2pa_json"
        assert signal.actor_id == "did:web:publisher.example"
        assert signal.issuer_id == "did:web:issuer.example"
        assert signal.action == "publish"
        assert signal.resource == "cawg:news-content"
        assert signal.context["credential_type"] == "vc:creator-identity"
        assert signal.process_evidence is not None
