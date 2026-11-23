"""Validate the archived replay's known freshness-semantic incompatibility.

The v1.3.0 bundle records a revocation feed dated after the historical
assessment. Rewriting the released bundle would destroy its evidence identity.
Under the corrected verifier, that feed cannot support a 'fresh' result.
Keep the older evidence unchanged; require precisely this observed mismatch.
"""

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from cawg_trqp_refimpl import mock_service
from cawg_trqp_refimpl.replay import replay_audit_bundle
from cawg_trqp_refimpl.validation import load_json


class _AssessmentClock(datetime):
    @classmethod
    def now(cls, tz=None):
        fixed = datetime(2026, 11, 24, tzinfo=timezone.utc)
        return fixed if tz is None else fixed.astimezone(tz)


def main() -> None:
    path = Path("examples/reproducibility_bundle_standard.json")
    bundle = load_json(path)
    assert bundle["bundle_id"] == (
        "urn:trqp:audit-bundle:sha256:"
        "7626b9bb606a5f6ced9dd9b92787ad4ffebf67db3935157ade1495615d609d61"
    ), "Archived evidence identity changed"
    with patch.object(mock_service, "datetime", _AssessmentClock):
        report = replay_audit_bundle(bundle, trusted_root=".")
    expected = [
        "policy_freshness: expected='fresh' actual='stale_but_warned'",
        "revocation_status: expected replay_inputs.revocation_status to match replayed policy_evidence.revocation_status",
    ]
    assert report.differences == expected, report.differences
    revocation = report.replayed_result["policy_evidence"]["revocation_status"]
    assert revocation["freshness_ok"] is False
    assert revocation["age_seconds"] is None
    print("Legacy replay: expected, bounded freshness incompatibility confirmed; archive not rewritten")


if __name__ == "__main__":
    main()
