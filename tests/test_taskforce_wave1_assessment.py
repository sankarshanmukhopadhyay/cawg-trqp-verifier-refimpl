"""Consumer-path tests with real local signatures and simulated external claims."""
import base64
import copy
import json
from pathlib import Path
from unittest.mock import patch

import pytest

from cawg_trqp_refimpl.experimental_taskforce_assessment import assess_operation
from cawg_trqp_refimpl.experimental_two_party_delegation import signing_bytes
from test_experimental_two_party_delegation import KEYS, PUBLIC, CONTEXT

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "conformance/delegated-creator-wave1-coverage.json").read_text())
CASES = CATALOG["cases"]


def inputs(case):
    request = {k: case[k] for k in ("principal", "actor", "action", "resource",
                                    "purpose", "consent_subject")}
    request.update(used_at="2026-11-23T00:00:00Z",
                   evaluated_at="2026-11-25T00:00:00Z", context_sha256=CONTEXT)
    statement = {"delegator": case["principal"], "delegate": case["actor"],
                 "actions": [case["action"]], "resources": [case["resource"]],
                 "purposes": [case["purpose"]],
                 "not_before": "2026-11-20T00:00:00Z",
                 "not_after": "2026-12-04T00:00:00Z"}
    envelope = {"statement": statement, "context_sha256": CONTEXT,
                "signatures": {role: {
                    "key_id": role, "signature_b64": base64.b64encode(key.sign(
                        signing_bytes(statement, CONTEXT, role, role))).decode()
                } for role, key in KEYS.items()}}
    records = []
    if case["consent_subject"]:
        records.append({
            "record_id": "private-record", "subject_ref": case["consent_subject"],
            "actions": [case["action"]], "resources": [case["resource"]],
            "purposes": [case["purpose"]], "valid_from": "2026-11-20T00:00:00Z",
            "valid_until": "2026-12-04T00:00:00Z", "withdrawn_effective_at": None,
            "withdrawal_observed_at": None,
            "evidence_ref": "https://example.test/private/secret",
            "evidence_sha256": "b" * 64,
        })
    subject = {"subject": case["actor"], "kind": "pseudonymous",
               "unique_claim": True, "vouching": [{"issuer": "private-registry",
                    "kind": "professional", "claimed_status": "verified", "scope": "creator"}]}
    return request, envelope, records, subject


def evaluate(request, envelope, records, subject, keys=PUBLIC):
    return assess_operation(request, envelope, keys,
                            consent_records=records, subject_evidence=subject)


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_wave1_consumer_path_and_adversarial_scope(case):
    req, env, records, subject = inputs(case)
    with patch("socket.socket.connect", side_effect=AssertionError("network prohibited")):
        result = evaluate(req, env, records, subject)
    assert result["statement_integrity"] == "verified"
    assert result["delegation_at_use"] == "signed_terms_in_scope"
    assert result["assured_authority"] == result["assured_consent"] == "indeterminate"
    assert result["subject_binding"] == "indeterminate"
    assert result["registry_recognition"] == "not_checked"
    assert result["consent_at_use"] == ("claimed_in_scope" if records else "indeterminate")
    output = json.dumps(result)
    for private in ("private-record", "private-registry", "https://example.test",
                    "opaque:", "pairwise:"):
        assert private not in output
    for field in ("principal", "actor", "action", "resource", "purpose"):
        changed = dict(req, **{field: "wrong-value"})
        other = evaluate(changed, env, records, subject)
        assert other["statement_integrity"] == "verified"
        assert other["delegation_at_use"] == "signed_terms_out_of_scope"
        assert other["assured_authority"] == "indeterminate"


def test_independent_consent_and_withdrawal():
    req, env, records, subject = inputs(CASES[0])
    records[0].update(withdrawn_effective_at="2026-11-24T00:00:00Z",
                      withdrawal_observed_at="2026-11-24T12:00:00Z")
    report = evaluate(req, env, records, subject)
    assert report["delegation_current"] == "signed_terms_in_scope"
    assert report["consent_at_use"] == "claimed_in_scope"
    assert report["consent_current"] == "claimed_withdrawn"
    assert report["assured_consent"] == "indeterminate"
    bad = copy.deepcopy(env)
    bad["signatures"].pop("delegate")
    report = evaluate(req, bad, records, subject)
    assert report["statement_integrity"] == "invalid"
    assert report["consent_current"] == "claimed_withdrawn"


def test_contradictory_missing_and_wrong_subject():
    req, env, records, subject = inputs(CASES[0])
    assert evaluate(req, env, [], subject)["consent_evidence_status"] == "missing"
    assert evaluate(req, env, records * 2, subject)["consent_evidence_status"] == "contradictory"
    report = evaluate(req, env, records, dict(subject, subject="different-subject"))
    assert report["subject_evidence_status"] == "subject_mismatch"
    report = evaluate(dict(req, consent_subject="another-person"), env, records, subject)
    assert report["consent_at_use"] == "claimed_out_of_scope"


def test_time_and_unknown_keys():
    req, env, records, subject = inputs(CASES[0])
    expired = evaluate(dict(req, evaluated_at="2026-12-04T00:00:00Z"), env, records, subject)
    assert expired["delegation_at_use"] == "signed_terms_in_scope"
    assert expired["delegation_current"] == "signed_terms_out_of_scope"
    assert expired["consent_current"] == "claimed_expired"
    unknown = evaluate(req, env, records, subject, keys={})
    assert unknown["statement_integrity"] == "indeterminate"
    assert unknown["delegation_at_use"] == "indeterminate"
    invalid = evaluate(dict(req, evaluated_at="2026-11-22T00:00:00Z"), env, records, subject)
    assert invalid["request_status"] == "invalid"


def test_crosswalk_references_existing_baselines():
    assert len(CASES) == 6
    assert len({case["id"] for case in CASES}) == 6
    assert CATALOG["required_questions"] == ["Q5", "Q6", "Q9", "Q10"]
    for case in CASES:
        source = json.loads((ROOT / case["source"]).read_text())
        assert case["baseline"] in {
            item.get("id", item.get("name")) for item in source["scenarios"]
        }
