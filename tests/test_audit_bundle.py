import json
from pathlib import Path

from cawg_trqp_refimpl.audit import build_audit_bundle
from cawg_trqp_refimpl.gateway import TrustGateway
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.verifier import Verifier


def _load_request(path="examples/verification_request.json"):
    return VerificationRequest(**json.loads(Path(path).read_text(encoding="utf-8")))


def test_audit_bundle_contains_policy_and_process_data():
    request = _load_request()
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(request)
    bundle = build_audit_bundle(request, result).to_dict()
    assert bundle["bundle_type"] == "cawg-trqp-audit-bundle"
    assert bundle["verification_result"]["trust_outcome"] == "trusted"
    assert bundle["policy_evidence"]["authorization_evidence"]
    assert bundle["process_appraisal"]["status"] == "verified"


def test_gateway_mediation_is_exported_in_bundle():
    request = _load_request()
    service = MockTRQPService(Path("data/policies.json"))
    verifier = Verifier(service=service, gateway=TrustGateway(service, gateway_id="gateway:test"))
    result = verifier.verify(request)
    bundle = build_audit_bundle(request, result).to_dict()
    assert bundle["gateway_mediation"]["gateway_id"] == "gateway:test"
