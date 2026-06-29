import copy
import json
from pathlib import Path

import pytest

from cawg_trqp_refimpl.audit import build_audit_bundle
from cawg_trqp_refimpl.feed_descriptor import validate_feed_descriptor
from cawg_trqp_refimpl.http_service import HTTPTRQPService
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.replay import replay_audit_bundle
from cawg_trqp_refimpl.verifier import Verifier


def _request() -> VerificationRequest:
    return VerificationRequest(**json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8")))


def _client():
    service = HTTPTRQPService(
        policy_path=Path("data/policies.json"),
        revocation_path=Path("data/revocations.json"),
        debug=False,
    )
    service.app.config["TESTING"] = True
    return service.app.test_client()


def test_http_rejects_profile_filesystem_reference():
    payload = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))
    payload["profile"] = "profiles/high_assurance.json"
    response = _client().post("/trqp/verify", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 400
    assert response.get_json()["error"] == "invalid_request"


def test_http_rejects_non_json_request_body():
    response = _client().post("/trqp/authorization", data="not-json", content_type="text/plain")
    assert response.status_code == 415
    assert response.get_json()["error"] == "invalid_request"


def test_high_assurance_fails_closed_without_feed_descriptors():
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(_request(), profile="high_assurance")
    assert result.verification_mode == "transport_guardrail"
    assert result.trust_outcome == "rejected"
    assert "missing_feed_descriptor" in result.explanations[0]


def test_high_assurance_accepts_valid_feed_descriptors():
    verifier = Verifier(service=MockTRQPService(
        Path("data/policies.json"),
        Path("data/revocations.json"),
        policy_descriptor_path="examples/feed_descriptors/policy-feed.signed.json",
        revocation_descriptor_path="examples/feed_descriptors/revocation-feed.signed.json",
    ))
    result = verifier.verify(_request(), profile="high_assurance")
    assert result.trust_outcome == "trusted"
    assert result.policy_evidence["feed_descriptors"]["policy"]["reason_code"] == "fresh"
    assert result.policy_evidence["feed_descriptors"]["revocation"]["reason_code"] == "fresh"


def test_descriptor_malformed_timestamp_is_stable_reason_code():
    descriptor = copy.deepcopy(json.loads(Path("examples/feed_descriptors/policy-feed.signed.json").read_text()))
    descriptor["valid_until"] = "not-a-timestamp"
    report = validate_feed_descriptor(
        descriptor,
        Path("data/policies.json").read_text(),
        trust_anchors=json.loads(Path("data/trust_anchors.json").read_text()),
        expected_authorities={"did:web:media-registry.example"},
    )
    assert report.reason_code == "descriptor_malformed"
    assert report.freshness_ok is False


def test_replay_rejects_bundle_policy_path_outside_trusted_root():
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(_request(), profile="standard")
    bundle = build_audit_bundle(
        _request(),
        result,
        profile="standard",
        policy_path="data/policies.json",
        revocation_path="data/revocations.json",
    ).to_dict()
    bundle["replay_inputs"]["policy_feed"]["policy_source"] = "/tmp/outside-policy.json"
    with pytest.raises(ValueError, match="trusted replay root"):
        replay_audit_bundle(bundle)


def test_replay_rejects_bundle_policy_digest_mismatch():
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(_request(), profile="standard")
    bundle = build_audit_bundle(
        _request(),
        result,
        profile="standard",
        policy_path="data/policies.json",
        revocation_path="data/revocations.json",
    ).to_dict()
    bundle["replay_inputs"]["policy_feed"]["policy_source_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="digest mismatch"):
        replay_audit_bundle(bundle)
