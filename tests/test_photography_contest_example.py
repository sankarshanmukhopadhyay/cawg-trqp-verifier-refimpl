import json
from pathlib import Path

from cawg_trqp_refimpl.feed_descriptor import load_feed_descriptor, validate_feed_descriptor
from cawg_trqp_refimpl.replay import replay_audit_bundle

EXAMPLE = Path("examples/photography_contest")


def test_photography_contest_example_replays_with_signed_feed_descriptors():
    bundle = json.loads((EXAMPLE / "replay_bundle.json").read_text(encoding="utf-8"))
    report = replay_audit_bundle(bundle)
    assert report.matches is True
    assert report.replayed_result["trust_outcome"] == "trusted"
    assert report.replayed_result["policy_evidence"]["feed_descriptors"]["policy"]["reason_code"] == "fresh"
    assert report.replayed_result["policy_evidence"]["feed_descriptors"]["revocation"]["reason_code"] == "fresh"


def test_photography_contest_decision_receipt_aligns_with_replay_bundle():
    receipt = json.loads((EXAMPLE / "decision_receipt.json").read_text(encoding="utf-8"))
    bundle = json.loads((EXAMPLE / "replay_bundle.json").read_text(encoding="utf-8"))
    assert receipt["decision"]["result"] == bundle["verification_result"]["trust_outcome"]
    assert receipt["evidence"]["replayable"] is True
    assert "feed_descriptors_valid" in receipt["decision"]["reasons"]


def test_photography_contest_feed_descriptors_validate_against_demo_trust_anchor():
    trust_anchors = json.loads((EXAMPLE / "trust_anchors.json").read_text(encoding="utf-8"))
    policy_report = validate_feed_descriptor(
        load_feed_descriptor(EXAMPLE / "policy-feed.signed.json"),
        (EXAMPLE / "contest_policy_feed.json").read_text(encoding="utf-8"),
        trust_anchors=trust_anchors,
        expected_authorities={"did:web:media-registry.example"},
    )
    revocation_report = validate_feed_descriptor(
        load_feed_descriptor(EXAMPLE / "revocation-feed.signed.json"),
        (EXAMPLE / "contest_revocation_feed.json").read_text(encoding="utf-8"),
        trust_anchors=trust_anchors,
        expected_authorities={"did:web:media-registry.example"},
    )
    assert policy_report.reason_code == "fresh"
    assert revocation_report.reason_code == "fresh"
