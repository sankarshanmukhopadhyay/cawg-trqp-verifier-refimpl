"""Deterministic local cryptographic tests; fixture keys are not trust roots."""
import base64
import json

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from cawg_trqp_refimpl.experimental_two_party_delegation import (
    signing_bytes, verify_two_party,
)

KEYS = {role: Ed25519PrivateKey.from_private_bytes(bytes([i]) * 32)
        for i, role in enumerate(("delegator", "delegate"), 1)}
PUBLIC = {role: key.public_key().public_bytes(
    serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    for role, key in KEYS.items()}
CONTEXT = "a" * 64


def signed():
    statement = {
        "delegator": "opaque:principal", "delegate": "opaque:recipient",
        "actions": ["publish"], "resources": ["asset:1"], "purposes": ["news"],
        "not_before": "2026-11-20T00:00:00Z", "not_after": "2026-12-04T00:00:00Z",
    }
    return {
        "statement": statement, "context_sha256": CONTEXT,
        "signatures": {role: {
            "key_id": role, "signature_b64": base64.b64encode(
                key.sign(signing_bytes(statement, CONTEXT, role, role))
            ).decode()
        } for role, key in KEYS.items()},
    }


def check(envelope, keys=PUBLIC, context=CONTEXT):
    return verify_two_party(envelope, keys, expected_context_sha256=context)


def test_integrity_does_not_elevate_authority_or_consent():
    result = check(signed())
    assert result["statement_integrity"] == "verified"
    for field in ("assured_authority", "assured_consent",
                  "delegator_binding", "delegate_binding"):
        assert result[field] == "indeterminate"
    assert result["c2pa_binding"] == "not_checked"
    assert result["trusted_signing_time"] == "not_checked"
    assert result["status_evidence"] == "not_checked"
    assert "opaque:" not in json.dumps(result)


@pytest.mark.parametrize("field,value", [
    ("delegator", "impostor"), ("delegate", "impostor"),
    ("actions", ["create"]), ("resources", ["asset:2"]),
    ("purposes", ["advertising"]), ("not_after", "2027-01-01T00:00:00Z"),
])
def test_term_substitution(field, value):
    envelope = signed()
    envelope["statement"][field] = value
    assert check(envelope)["statement_integrity"] == "invalid"


def test_missing_or_swapped_roles():
    envelope = signed()
    del envelope["signatures"]["delegate"]
    assert check(envelope)["statement_integrity"] == "invalid"
    envelope = signed()
    a, b = envelope["signatures"].values()
    envelope["signatures"] = {"delegator": b, "delegate": a}
    assert check(envelope)["statement_integrity"] == "invalid"


def test_context_substitution_and_unknown_key():
    assert check(signed(), context="b" * 64)["statement_integrity"] == "invalid"
    envelope = signed()
    envelope["context_sha256"] = "b" * 64
    assert check(envelope, context="b" * 64)["statement_integrity"] == "invalid"
    assert check(signed(), {})["statement_integrity"] == "indeterminate"


def test_same_key_under_two_aliases_cannot_pass():
    envelope = signed()
    envelope["signatures"]["delegate"]["signature_b64"] = base64.b64encode(
        KEYS["delegator"].sign(signing_bytes(
            envelope["statement"], CONTEXT, "delegate", "delegate"))
    ).decode()
    assert check(envelope, {"delegator": PUBLIC["delegator"],
                            "delegate": PUBLIC["delegator"]})["statement_integrity"] == "invalid"


def test_caller_cannot_inject_verified_claims():
    envelope = signed()
    envelope["assured_consent"] = True
    assert check(envelope)["statement_integrity"] == "invalid"
