import json
from pathlib import Path

from cawg_trqp_refimpl.audit import build_audit_bundle
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.verifier import Verifier


def test_audit_bundle_carries_feed_descriptor_evidence_into_replay_inputs():
    request = VerificationRequest(**json.loads(Path("examples/verification_request.json").read_text()))
    verifier = Verifier(service=MockTRQPService(
        Path("data/policies.json"),
        Path("data/revocations.json"),
        policy_descriptor_path="examples/feed_descriptors/policy-feed.signed.json",
        revocation_descriptor_path="examples/feed_descriptors/revocation-feed.signed.json",
    ))
    result = verifier.verify(request)
    bundle = build_audit_bundle(request, result, policy_path="data/policies.json", revocation_path="data/revocations.json").to_dict()
    assert bundle["policy_evidence"]["feed_descriptors"]["policy"]["reason_code"] == "fresh"
    assert bundle["replay_inputs"]["feed_descriptors"]["revocation"]["reason_code"] == "fresh"
