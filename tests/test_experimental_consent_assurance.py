"""Consent evidence cannot silently become legal or verified permission."""
from copy import deepcopy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from cawg_trqp_refimpl.experimental_consent_assurance import (
    InvalidConsentCase, assess_consent,
)

SCHEMA = json.loads((Path(__file__).resolve().parents[1] /
                     "schemas/experimental-consent-assurance.schema.json").read_text())


def sample():
    return {
        "case_id": "brand-voice", "subject_ref": "subject-pairwise-1",
        "action": "publish", "resource": "campaign-1", "purpose": "advertising",
        "used_at": "2026-10-10T00:00:00Z", "evaluated_at": "2026-10-11T00:00:00Z",
        "records": [{
            "record_id": "consent-1", "subject_ref": "subject-pairwise-1",
            "actions": ["publish"], "resources": ["campaign-1"],
            "purposes": ["advertising"], "valid_from": "2026-10-01T00:00:00Z",
            "valid_until": "2026-10-31T00:00:00Z",
            "withdrawn_effective_at": None, "withdrawal_observed_at": None,
            "evidence_ref": "https://example.test/private/consent",
            "evidence_sha256": "a" * 64,
        }],
    }


def test_schema_and_no_false_verified_consent():
    Draft202012Validator.check_schema(SCHEMA)
    report = assess_consent(sample())
    Draft202012Validator(SCHEMA).validate(report)
    assert report["consent_evidence_status"] == "unverified"
    assert report["consent_at_use_time"] == "claimed_in_scope"
    assert report["assured_consent"] == "indeterminate"
    assert "subject_ref" not in report
    assert "evidence_ref" not in report
    report["assured_consent"] = "verified"
    with pytest.raises(Exception):
        Draft202012Validator(SCHEMA).validate(report)


def test_missing_and_scope_mismatch():
    c = sample()
    c["records"] = []
    assert assess_consent(c)["consent_evidence_status"] == "missing"
    c = sample()
    c["purpose"] = "training"
    report = assess_consent(c)
    assert report["consent_scope_status"] == "outside_claimed_scope"
    assert report["consent_at_use_time"] == "claimed_out_of_scope"
    assert report["assured_consent"] == "indeterminate"


def test_subject_mismatch_is_not_accepted():
    c = sample()
    c["subject_ref"] = "different-subject"
    assert assess_consent(c)["reason"] == "no_matching_consent_scope"


def test_duplicate_records_are_contradictory_not_verified():
    c = sample()
    c["records"].append(deepcopy(c["records"][0]))
    report = assess_consent(c)
    assert report["consent_evidence_status"] == "contradictory"
    assert report["assured_consent"] == "indeterminate"


@pytest.mark.parametrize("field,value", [
    ("used_at", "2026-10-10T00:00:00"),
    ("records", "not a list"),
    ("extra", "unsupported"),
])
def test_invalid_input_is_rejected(field, value):
    c = sample()
    c[field] = value
    with pytest.raises(InvalidConsentCase):
        assess_consent(c)


def test_replay_is_deterministic():
    c = sample()
    assert assess_consent(c) == assess_consent(deepcopy(c))
