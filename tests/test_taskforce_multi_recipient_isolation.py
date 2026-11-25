"""Q23: independent recipient grants, not a new multi-party wire format."""
import base64
import copy
import sys
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from cawg_trqp_refimpl.experimental_taskforce_assessment import assess_operation
from cawg_trqp_refimpl.experimental_two_party_delegation import signing_bytes

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from taskforce_wave1_fixtures import CASES, KEYS, PUBLIC, CONTEXT, inputs


def second_recipient(req, env, records):
    req = dict(req, actor="second-recipient", consent_subject="second-subject")
    env = copy.deepcopy(env)
    env["statement"]["delegate"] = req["actor"]
    keys = dict(KEYS, delegate=Ed25519PrivateKey.from_private_bytes(b"\x07" * 32))
    pins = {role: key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        for role, key in keys.items()}
    for role, key in keys.items():
        env["signatures"][role]["signature_b64"] = base64.b64encode(
            key.sign(signing_bytes(env["statement"], CONTEXT, role, role))).decode()
    return req, env, [], pins


def test_pending_and_accepted_recipients_do_not_share_signatures_or_consent():
    req_a, env_a, records_a, _ = inputs(CASES[0])
    req_b, env_b, records_b, pins_b = second_recipient(req_a, env_a, records_a)
    pending_b = copy.deepcopy(env_b)
    pending_b["signatures"].pop("delegate")
    a = assess_operation(req_a, env_a, PUBLIC, consent_records=records_a)
    b = assess_operation(req_b, pending_b, pins_b, consent_records=records_b)
    assert a["statement_integrity"] == "verified"
    assert b["statement_integrity"] == "invalid"
    assert b["consent_evidence_status"] == "missing"
    assert assess_operation(req_b, env_a, PUBLIC, consent_records=records_a)[
        "delegation_at_use"] == "signed_terms_out_of_scope"
    b = assess_operation(req_b, env_b, pins_b, consent_records=records_a)
    assert b["statement_integrity"] == "verified"
    assert b["consent_at_use"] == "claimed_out_of_scope"
    assert b["assured_consent"] == "indeterminate"


def test_renewing_one_recipient_does_not_renew_another():
    req_a, env_a, records_a, _ = inputs(CASES[0])
    req_b, env_b, _, pins_b = second_recipient(req_a, env_a, records_a)
    env_a["statement"]["not_after"] = "2026-12-20T00:00:00Z"
    for role, key in KEYS.items():
        env_a["signatures"][role]["signature_b64"] = base64.b64encode(
            key.sign(signing_bytes(env_a["statement"], CONTEXT, role, role))).decode()
    now = "2026-12-04T00:00:00Z"
    a = assess_operation(dict(req_a, evaluated_at=now), env_a, PUBLIC)
    b = assess_operation(dict(req_b, evaluated_at=now), env_b, pins_b)
    assert a["delegation_current"] == "signed_terms_in_scope"
    assert b["delegation_current"] == "signed_terms_out_of_scope"
    assert a["assured_authority"] == b["assured_authority"] == "indeterminate"
