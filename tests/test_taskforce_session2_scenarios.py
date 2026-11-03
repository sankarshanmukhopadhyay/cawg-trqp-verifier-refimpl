"""Session 2 feasibility vectors. No live subject/issuer or uniqueness proof."""
import copy
import json
from pathlib import Path

import pytest
from cawg_trqp_refimpl.experimental_subject_evidence import assess_subject_evidence
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate
from cawg_trqp_refimpl.taskforce_scenarios import make_case

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "conformance/delegated-creator-session2-scenarios.json").read_text())


def test_three_distinct_scenarios():
    assert DATA["schema_version"] == "0.1"
    assert len(DATA["scenarios"]) == 3
    assert len({row["id"] for row in DATA["scenarios"]}) == 3


def test_human_manager_delegation_and_non_elevation():
    row = DATA["scenarios"][0]
    case = make_case(dict(name=row["id"], root=row["root"], actor=row["delegate"],
                          action=row["action"], resource=row["resource"],
                          purpose=row["purpose"], sign=row["sign"], now=row["now"],
                          start=row["start"], end=row["end"],
                          links=[[row["root"], row["delegate"]]]))
    result = evaluate(case)
    assert result["historical_authority"] == "authorized"  # local simulation
    assert result["assured_authority"] == "indeterminate"
    assert result["assured_coverage"] == "unverified"
    assert result == evaluate(copy.deepcopy(case))
    case["action"] = "create"
    assert evaluate(case)["reason"] == "requested_action_out_of_scope"
    case["action"] = row["action"]
    case["chain"][0]["revoked_at"] = "2026-10-22T00:00:00Z"
    assert evaluate(case)["reason"] == "revoked_at_signing"
    case["chain"][0]["revoked_at"] = None
    case["actor"] = "other-manager"
    assert evaluate(case)["reason"] == "actor_not_delegate"


@pytest.mark.parametrize("row", DATA["scenarios"][1:], ids=lambda r:r["id"])
def test_subject_claims_do_not_authorize(row):
    result = assess_subject_evidence({
        "subject": row["subject"], "kind": row["subject_kind"],
        "unique_claim": row["unique_claim"], "vouching": row["vouching"]
    })
    assert result["assured_subject_binding"] == "indeterminate"
    assert result["assured_uniqueness"] == "indeterminate"
    assert result["assured_authority"] == "indeterminate"
    assert result["assured_vouching"] == "unverified"
    assert result["evidence_origin"] == "caller_supplied_simulation"
    assert result == assess_subject_evidence({
        "subject": row["subject"], "kind": row["subject_kind"],
        "unique_claim": row["unique_claim"], "vouching": copy.deepcopy(row["vouching"])
    })


def test_credential_revocation_conflict_and_unknown_issuer_never_elevate():
    row = DATA["scenarios"][2]
    for claimed_status in ("verified", "revoked", "contradictory", "indeterminate"):
        v = copy.deepcopy(row["vouching"])
        v[0]["claimed_status"] = claimed_status
        result = assess_subject_evidence({
            "subject": row["subject"], "kind": row["subject_kind"],
            "unique_claim": False, "vouching": v
        })
        assert result["assured_authority"] == "indeterminate"
        assert result["assured_vouching"] == "unverified"
        assert result["vouching_sources"][0]["recognition"] == "not_checked"


@pytest.mark.parametrize("broken", [
    {"subject":"", "kind":"pseudonymous", "unique_claim":True, "vouching":[]},
    {"subject":"x", "kind":"pseudonymous", "unique_claim":"yes", "vouching":[]},
    {"subject":"x", "kind":"unknown", "unique_claim":True, "vouching":[]},
    {"subject":"x", "kind":"identified", "unique_claim":False, "vouching":[{"issuer":"i","kind":"public","claimed_status":"authorized","scope":"creator"}]},
])
def test_malformed_claims_are_rejected(broken):
    with pytest.raises(ValueError):
        assess_subject_evidence(broken)
