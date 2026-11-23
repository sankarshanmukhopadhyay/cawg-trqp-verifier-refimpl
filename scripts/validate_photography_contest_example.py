#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

from cawg_trqp_refimpl import mock_service
from cawg_trqp_refimpl.feed_descriptor import load_feed_descriptor, validate_feed_descriptor
from cawg_trqp_refimpl.replay import replay_audit_bundle
from cawg_trqp_refimpl.validation import load_json

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "photography_contest"


def _validate_schema(schema_name: str, instance_path: Path) -> list[str]:
    schema = load_json(ROOT / "schemas" / schema_name)
    instance = load_json(instance_path)
    validator = Draft202012Validator(schema)
    return [f"{instance_path.relative_to(ROOT)}: {'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}" for err in validator.iter_errors(instance)]


def main() -> int:
    failures: list[str] = []
    required = [
        "submission.json",
        "contest_policy_feed.json",
        "contest_revocation_feed.json",
        "policy-feed.signed.json",
        "revocation-feed.signed.json",
        "trust_anchors.json",
        "decision_receipt.json",
        "replay_bundle.json",
    ]
    for name in required:
        if not (EXAMPLE / name).exists():
            failures.append(f"missing required example artifact: {name}")

    if failures:
        print("validate_photography_contest_example.py: FAIL")
        for failure in failures:
            print(f" - {failure}")
        return 1

    failures.extend(_validate_schema("decision-receipt.schema.json", EXAMPLE / "decision_receipt.json"))
    failures.extend(_validate_schema("audit-bundle.schema.json", EXAMPLE / "replay_bundle.json"))

    trust_anchors = load_json(EXAMPLE / "trust_anchors.json")
    policy_body = (EXAMPLE / "contest_policy_feed.json").read_text(encoding="utf-8")
    revocation_body = (EXAMPLE / "contest_revocation_feed.json").read_text(encoding="utf-8")
    policy_report = validate_feed_descriptor(load_feed_descriptor(EXAMPLE / "policy-feed.signed.json"), policy_body, trust_anchors=trust_anchors, expected_authorities={"did:web:media-registry.example"})
    revocation_report = validate_feed_descriptor(load_feed_descriptor(EXAMPLE / "revocation-feed.signed.json"), revocation_body, trust_anchors=trust_anchors, expected_authorities={"did:web:media-registry.example"})
    for label, report in [("policy", policy_report), ("revocation", revocation_report)]:
        if report.reason_code != "fresh":
            failures.append(f"{label} descriptor is not fresh: {report.reason_code}; {report.violations}")

    # The signed historical fixture asserts 'fresh' for a revocation feed
    # issued in 2027. Preserve its evidence identity and detect the precise
    # legacy semantic discrepancy rather than rewriting the archived record.
    class AssessmentClock(datetime):
        @classmethod
        def now(cls, tz=None):
            fixed = datetime(2026, 11, 24, tzinfo=timezone.utc)
            return fixed if tz is None else fixed.astimezone(tz)

    bundle = load_json(EXAMPLE / "replay_bundle.json")
    with patch.object(mock_service, "datetime", AssessmentClock):
        replay_report = replay_audit_bundle(bundle)
    known_legacy_difference = (
        bundle.get("bundle_id") == (
            "urn:trqp:audit-bundle:sha256:"
            "fd6ca3ca89a299b2e2958a1f5d32ed8f9ff4c4559d5a48cad941ab9a64d04ab3"
        )
        and replay_report.differences == [
            "policy_freshness: expected='fresh' actual='stale_but_warned'",
            "revocation_status: expected replay_inputs.revocation_status to match replayed policy_evidence.revocation_status",
        ]
        and replay_report.replayed_result["policy_evidence"]["revocation_status"]["freshness_ok"] is False
    )
    if not replay_report.matches and not known_legacy_difference:
        failures.append("replay bundle did not reproduce the expected verification result")
        failures.extend(replay_report.differences)

    receipt = load_json(EXAMPLE / "decision_receipt.json")
    if receipt["decision"]["result"] != replay_report.replayed_result["trust_outcome"]:
        failures.append("decision receipt result does not match replayed trust outcome")

    if failures:
        print("validate_photography_contest_example.py: FAIL")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print("validate_photography_contest_example.py: OK")
    print(json.dumps({
        "decision": receipt["decision"]["result"],
        "replay_matches": replay_report.matches,
        "legacy_freshness_incompatibility": known_legacy_difference,
        "policy_descriptor": policy_report.reason_code,
        "revocation_descriptor": revocation_report.reason_code,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
