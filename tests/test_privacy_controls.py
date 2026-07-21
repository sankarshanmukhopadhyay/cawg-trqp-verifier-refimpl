import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from cawg_trqp_refimpl.audit import build_audit_bundle
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.privacy import load_privacy_profile, validate_context
from cawg_trqp_refimpl.verifier import Verifier


def _request():
    return VerificationRequest(**json.loads(Path("examples/verification_request.json").read_text()))


def _result(request):
    return Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json"))).verify(request)


def test_privacy_profiles_validate():
    schema = json.loads(Path("schemas/privacy-profile.schema.json").read_text())
    validator = Draft202012Validator(schema)
    for path in Path("profiles/privacy").glob("*.json"):
        assert list(validator.iter_errors(json.loads(path.read_text()))) == []


def test_minimal_receipt_redacts_raw_identifiers():
    request = _request()
    bundle = build_audit_bundle(request, _result(request), privacy_profile="minimal_receipt").to_dict()
    replay_request = bundle["replay_inputs"]["request"]
    assert "entity_id" not in replay_request
    assert replay_request["entity_id_digest"].startswith("hmac-sha256:")
    assert bundle["replay_inputs"]["privacy"]["contains_raw_request"] is False


def test_replay_bundle_retains_request_for_authorized_replay():
    request = _request()
    bundle = build_audit_bundle(request, _result(request), privacy_profile="replay_bundle").to_dict()
    assert bundle["replay_inputs"]["request"]["entity_id"] == request.entity_id
    assert bundle["replay_inputs"]["privacy"]["access_scope"] == "trqp.audit.export"


def test_context_allow_list_rejects_unapproved_fields():
    with pytest.raises(ValueError):
        validate_context({"territory": "US", "email": "person@example.com"}, {"territory"})


def test_retention_and_context_examples_validate():
    pairs = [
        ("schemas/retention-policy.schema.json", "examples/privacy/retention-policy.json"),
        ("schemas/context-profile.schema.json", "examples/privacy/context-profile.json"),
        ("schemas/redaction-policy.schema.json", "examples/privacy/redaction-policy.json"),
    ]
    for schema_path, example_path in pairs:
        validator = Draft202012Validator(json.loads(Path(schema_path).read_text()))
        assert list(validator.iter_errors(json.loads(Path(example_path).read_text()))) == []


@pytest.mark.skipif(pytest.importorskip("flask") is None, reason="Flask unavailable")
def test_full_replay_export_requires_scope():
    from cawg_trqp_refimpl.http_service import HTTPTRQPService
    service = HTTPTRQPService(Path("data/policies.json"), Path("data/revocations.json"), debug=True)
    client = service.app.test_client()
    payload = json.loads(Path("examples/verification_request.json").read_text())
    payload["privacy_profile"] = "replay_bundle"
    denied = client.post("/trqp/audit-bundle", json=payload)
    assert denied.status_code == 403
    allowed = client.post("/trqp/audit-bundle", json=payload, headers={"X-TRQP-Scopes": "trqp.audit.export"})
    assert allowed.status_code == 200
