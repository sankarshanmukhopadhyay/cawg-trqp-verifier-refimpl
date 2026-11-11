"""Two synthetic cross-taskforce cases preserve independent evidence boundaries."""
from copy import deepcopy
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from cawg_trqp_refimpl.experimental_consent_assurance import assess_consent
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate
from cawg_trqp_refimpl.taskforce_scenarios import read_scenarios, make_case

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "conformance/delegated-creator-consent-scenarios.json").read_text())
SCHEMA = json.loads((ROOT / "schemas/experimental-consent-assurance.schema.json").read_text())


def test_two_integrated_scenarios_are_portable_and_do_not_elevate_evidence():
    assert CATALOG["schema_version"] == "0.1"
    assert len(CATALOG["scenarios"]) == 2
    worlds = {row["name"]: row for row in read_scenarios()}
    for row in CATALOG["scenarios"]:
        delegated = evaluate(make_case(worlds[row["delegation_world"]]))
        consent = assess_consent(row["consent_case"])
        Draft202012Validator(SCHEMA).validate(consent)
        assert delegated["historical_authority"] == "authorized"
        assert delegated["assured_authority"] == "indeterminate"
        assert consent["consent_at_use_time"] == "claimed_in_scope"
        assert consent["assured_consent"] == "indeterminate"
        assert consent["consent_evidence_status"] == "unverified"


def test_valid_delegation_never_fills_missing_consent():
    row = CATALOG["scenarios"][0]
    worlds = {r["name"]: r for r in read_scenarios()}
    assert evaluate(make_case(worlds[row["delegation_world"]]))["historical_authority"] == "authorized"
    case = deepcopy(row["consent_case"])
    case["records"] = []
    assert assess_consent(case)["consent_evidence_status"] == "missing"


def test_matching_consent_claim_does_not_fix_unauthorized_delegate():
    row = CATALOG["scenarios"][1]
    worlds = {r["name"]: r for r in read_scenarios()}
    delegation = make_case(worlds[row["delegation_world"]])
    delegation["resource"] = "other-album"
    assert evaluate(delegation)["authority"] == "denied"
    assert assess_consent(row["consent_case"])["consent_at_use_time"] == "claimed_in_scope"


def test_out_of_scope_purpose_and_tool_or_resource_are_rejected_as_claims():
    for row in CATALOG["scenarios"]:
        case = deepcopy(row["consent_case"])
        case["purpose"] = "ai-training"
        assert assess_consent(case)["consent_scope_status"] == "outside_claimed_scope"
        case = deepcopy(row["consent_case"])
        case["resource"] = "unauthorized-other-project"
        assert assess_consent(case)["consent_at_use_time"] == "claimed_out_of_scope"


def test_future_use_after_withdrawal_is_not_claimed_in_scope():
    row = CATALOG["scenarios"][1]
    case = deepcopy(row["consent_case"])
    record = case["records"][0]
    record["withdrawn_effective_at"] = "2026-10-22T00:00:00Z"
    record["withdrawal_observed_at"] = "2026-10-22T12:00:00Z"
    assert assess_consent(case)["consent_at_use_time"] == "claimed_out_of_scope"


def test_machine_readable_demo_is_deterministic_and_redacted():
    command = [sys.executable, str(ROOT / "scripts/run_taskforce_consent_demo.py")]
    first = subprocess.check_output(command, cwd=ROOT)
    assert first == subprocess.check_output(command, cwd=ROOT)
    report = json.loads(first)
    assert report["independent_consent_verification"] is False
    assert report["independent_interoperability"] is False
    assert report["all_match"] is True
    assert len(report["results"]) == 2
    assert "performer:voice" not in first.decode()
    for result in report["results"]:
        Draft202012Validator(SCHEMA).validate(result["consent"])
        assert result["consent"]["assured_consent"] == "indeterminate"
