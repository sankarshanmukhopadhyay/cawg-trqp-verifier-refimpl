"""Portable five-world taskforce story corpus; normalized synthetic inputs only."""
import copy
import json
from pathlib import Path
import pytest
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate
from cawg_trqp_refimpl.taskforce_scenarios import make_case

DATA = json.loads((Path(__file__).resolve().parents[1] / "conformance" / "delegated-creator-five-world-scenarios.json").read_text())
@pytest.mark.parametrize("row", DATA["scenarios"], ids=lambda row: row["name"])
def test_story_positive_and_negative(row):
    c = make_case(row)
    result = evaluate(c)
    assert result["historical_authority"] == row["expect"]
    assert result["current_authority"] == row["current"]
    assert result["evidence_provenance"]["delegator_signature"] == "not_verified"
    assert result["evidence_provenance"]["signing_time"] == "caller_supplied_untrusted"
    assert result["coverage"] == "delegator-covered"  # simulated label only
    assert result["generator"] == "accepted"
    assert not any(key in result for key in ("agreement", "consent", "contract"))
    if row.get("creative_credit"):
        assert "creative_credit" not in result
    bad = copy.deepcopy(c)
    if row.get("negative"):
        bad["signed_at"] = row["negative"]
    elif row.get("negative_resource"):
        bad["resource"] = row["negative_resource"]
    elif row.get("negative_action"):
        bad["action"] = row["negative_action"]
    elif row.get("negative_redelegate"):
        bad["chain"][0]["redelegation"] = False
    assert evaluate(bad)["reason"] == row["negative_reason"]

def test_five_unique_worlds_and_reproducibility():
    assert len(DATA["scenarios"]) == 5
    assert len({r["world"] for r in DATA["scenarios"]}) == 5
    for row in DATA["scenarios"]:
        case = make_case(row)
        assert evaluate(case) == evaluate(copy.deepcopy(case))
