"""The public report contract forbids unsupported assurance elevation."""
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError

from test_experimental_taskforce_source_evidence import assess, evidence_inputs
from test_taskforce_wave1_assessment import CASES, inputs, evaluate

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/experimental-taskforce-operation.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA)


def test_schema_and_consumer_results():
    Draft202012Validator.check_schema(SCHEMA)
    for case in CASES:
        VALIDATOR.validate(evaluate(*inputs(case)))
    VALIDATOR.validate(assess(evidence_inputs()))
    req, env, records, subject = inputs(CASES[0])
    env["signatures"].pop("delegate")
    VALIDATOR.validate(evaluate(req, env, records, subject))
    VALIDATOR.validate(evaluate({}, env, records, subject))


@pytest.mark.parametrize("field,value", [
    ("assured_authority", "verified"), ("assured_consent", "verified"),
    ("subject_binding", "verified"), ("registry_recognition", "verified"),
    ("c2pa_binding", "verified"), ("guardian_authority", "verified"),
    ("private_reference", "https://example.test/private"),
])
def test_report_cannot_advertise_unsupported_assurance(field, value):
    report = assess(evidence_inputs())
    report[field] = value
    with pytest.raises(ValidationError):
        VALIDATOR.validate(report)


def test_unauthenticated_source_cannot_report_active():
    report = assess(evidence_inputs())
    report["source_evidence"]["delegate_binding"]["status"] = "stale"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(report)


def test_invalid_signature_cannot_report_signed_scope_success():
    report = assess(evidence_inputs())
    report["statement_integrity"] = "invalid"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(report)
