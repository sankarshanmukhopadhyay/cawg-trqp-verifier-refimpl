import json
from pathlib import Path

from cawg_trqp_refimpl.attestation import sign_audit_bundle_from_path
from cawg_trqp_refimpl.audit import build_audit_bundle
from cawg_trqp_refimpl.gateway import TrustGateway
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.replay import replay_audit_bundle
from cawg_trqp_refimpl.validation import load_json, validate_audit_bundle
from cawg_trqp_refimpl.verifier import Verifier



def _load_request(path="examples/verification_request.json"):
    return VerificationRequest(**json.loads(Path(path).read_text(encoding="utf-8")))



def test_audit_bundle_contains_policy_and_process_data():
    request = _load_request()
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(request)
    bundle = build_audit_bundle(
        request,
        result,
        profile="standard",
        policy_path="data/policies.json",
        revocation_path="data/revocations.json",
    ).to_dict()
    assert bundle["bundle_type"] == "cawg-trqp-audit-bundle"
    assert bundle["verification_result"]["trust_outcome"] == "trusted"
    assert bundle["policy_evidence"]["authorization_evidence"]
    assert bundle["process_appraisal"]["status"] == "verified"
    assert bundle["replay_inputs"]["profile"]["id"] == "standard"
    assert bundle["replay_inputs"]["policy_feed"]["policy_source"] == "data/policies.json"
    assert len(bundle["bundle_digest_sha256"]) == 64



def test_gateway_mediation_is_exported_in_bundle():
    request = _load_request()
    service = MockTRQPService(Path("data/policies.json"))
    verifier = Verifier(service=service, gateway=TrustGateway(service, gateway_id="gateway:test"))
    result = verifier.verify(request)
    bundle = build_audit_bundle(request, result, profile="standard", use_gateway=True).to_dict()
    assert bundle["gateway_mediation"]["gateway_id"] == "gateway:test"
    assert bundle["replay_inputs"]["use_gateway"] is True



def test_audit_bundle_schema_and_digest_validation_pass():
    request = _load_request()
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(request)
    bundle = build_audit_bundle(
        request,
        result,
        exported_at="2026-03-31T00:00:00Z",
        policy_path="data/policies.json",
        revocation_path="data/revocations.json",
    ).to_dict()
    schema = load_json("schemas/audit-bundle.schema.json")
    assert validate_audit_bundle(bundle, schema) == []



def test_audit_bundle_attestation_validation_passes():
    request = _load_request()
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(request)
    bundle = build_audit_bundle(
        request,
        result,
        exported_at="2026-03-31T00:00:00Z",
        policy_path="data/policies.json",
        revocation_path="data/revocations.json",
    ).to_dict()
    signed_bundle = sign_audit_bundle_from_path(bundle, Path("data/snapshot_signing_key.example.pem"), key_id="media-registry-snapshot-key-1")
    schema = load_json("schemas/audit-bundle.schema.json")
    assert validate_audit_bundle(signed_bundle, schema, trust_anchors_path="data/trust_anchors.json") == []



def test_audit_bundle_replay_matches_original_verification():
    request = _load_request()
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(request)
    bundle = build_audit_bundle(
        request,
        result,
        exported_at="2026-03-31T00:00:00Z",
        policy_path="data/policies.json",
        revocation_path="data/revocations.json",
    ).to_dict()
    report = replay_audit_bundle(bundle)
    assert report.matches is True
    assert report.differences == []
    assert report.policy_sources["policy_source"] == "data/policies.json"
