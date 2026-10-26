"""Schema evidence and scope regression for all five creative worlds."""
import copy
import json
import subprocess
import sys
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from cawg_trqp_refimpl.taskforce_scenarios import read_scenarios, make_case
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=json.loads((ROOT/"schemas/experimental-taskforce-report.schema.json").read_text())

def test_public_report_schema_and_no_elevation():
    report=json.loads(subprocess.check_output(
        [sys.executable,str(ROOT/"scripts/run_taskforce_five_world_demo.py")],cwd=ROOT))
    Draft202012Validator.check_schema(SCHEMA)
    Draft202012Validator(SCHEMA).validate(report)
    report["results"][0]["actual"]["assured_authority"]="authorized"
    with pytest.raises(Exception):
        Draft202012Validator(SCHEMA).validate(report)

@pytest.mark.parametrize("field,fixture_field", [
    ("action","action"),("resource","resource"),("purpose","purpose"),
])
def test_scope_boundaries(field,fixture_field):
    for row in read_scenarios():
        c=make_case(row)
        c[field]="outside-"+row[fixture_field]
        result=evaluate(c)
        assert result["reason"]=="requested_action_out_of_scope"
        assert result["assured_authority"]=="indeterminate"

@pytest.mark.parametrize("when,expected",[
    ("2026-10-01T00:00:00Z","authorized"),
    ("2026-09-30T23:59:59Z","denied"),
    ("2026-10-31T00:00:00Z","denied"),
])
def test_half_open_signing_interval(when,expected):
    row=next(x for x in read_scenarios() if x["name"]=="freelance-reporter")
    c=make_case(row)
    c["signed_at"]=when
    assert evaluate(c)["historical_authority"]==expected
