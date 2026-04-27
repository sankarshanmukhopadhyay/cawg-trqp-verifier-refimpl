import copy
import json
from pathlib import Path

from cawg_trqp_refimpl.feed_descriptor import validate_feed_descriptor
from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.verifier import Verifier

TRUST = json.loads(Path("data/trust_anchors.json").read_text())


def _descriptor(name: str) -> dict:
    return json.loads(Path(f"examples/feed_descriptors/{name}.signed.json").read_text())


def test_feed_descriptor_signature_digest_and_authority_pass():
    descriptor = _descriptor("policy-feed")
    report = validate_feed_descriptor(
        descriptor,
        Path(descriptor["feed"]["source"]).read_text(),
        trust_anchors=TRUST,
        expected_authorities={"did:web:media-registry.example"},
    )
    assert report.reason_code == "fresh"
    assert report.signature_ok is True
    assert report.integrity_ok is True
    assert report.authority_ok is True


def test_feed_descriptor_digest_mismatch_is_detected():
    descriptor = _descriptor("policy-feed")
    report = validate_feed_descriptor(descriptor, '{"tampered":true}', trust_anchors=TRUST, expected_authorities={"did:web:media-registry.example"})
    assert report.reason_code == "descriptor_digest_mismatch"
    assert report.integrity_ok is False


def test_feed_descriptor_signature_mismatch_is_detected():
    descriptor = copy.deepcopy(_descriptor("policy-feed"))
    descriptor["feed"]["source"] = "data/other.json"
    report = validate_feed_descriptor(descriptor, Path("data/policies.json").read_text(), trust_anchors=TRUST, expected_authorities={"did:web:media-registry.example"})
    assert report.reason_code == "descriptor_signature_invalid"


def test_runtime_exports_feed_descriptor_evidence():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_minimal.json"), "did:web:media-registry.example")
    verifier = Verifier(service=MockTRQPService(
        Path("data/policies.json"),
        Path("data/revocations.json"),
        policy_descriptor_path="examples/feed_descriptors/policy-feed.signed.json",
        revocation_descriptor_path="examples/feed_descriptors/revocation-feed.signed.json",
    ))
    result = verifier.verify(req, profile="standard")
    assert result.trust_outcome == "trusted"
    assert result.policy_freshness == "fresh"
    assert result.policy_evidence["feed_descriptors"]["policy"]["reason_code"] == "fresh"
