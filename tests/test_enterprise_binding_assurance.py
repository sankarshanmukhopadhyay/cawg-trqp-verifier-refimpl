"""Cryptographic statement integrity is not enterprise authorization."""
import base64
import copy
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cawg_trqp_refimpl.experimental_delegation_signature import canonical_bytes, verify_statement
from cawg_trqp_refimpl.experimental_binding_assurance import assess_signer_binding

KEY = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
PUB = KEY.public_key().public_bytes(
    encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
STATEMENT = {"delegator":"enterprise","delegate":"manager","actions":["publish"],
             "resources":["post:1"],"purposes":["advertising"],
             "not_before":"2026-10-01T00:00:00Z",
             "not_after":"2026-10-30T00:00:00Z"}
CLAIMS = {"subject_binding":"verified", "organizational_binding":"verified",
          "authority_to_bind":"verified"}


def signed():
    return {"statement": copy.deepcopy(STATEMENT), "key_id": "fixture:enterprise",
            "signature_b64": base64.b64encode(KEY.sign(canonical_bytes(STATEMENT))).decode()}


def test_real_signature_cannot_establish_organization_or_authority():
    proof = verify_statement(signed(), {"fixture:enterprise": PUB})
    assert proof["proof"] == "verified"
    result = assess_signer_binding(proof, CLAIMS)
    assert result["statement_integrity"] == "verified"
    assert result["subject_binding"] == "indeterminate"
    assert result["organizational_binding"] == "indeterminate"
    assert result["authority_to_bind"] == "indeterminate"
    assert result["delegated_authority"] == "indeterminate"
    assert result["assured_authority"] == "indeterminate"
    assert result["claim_provenance"] == "caller_supplied_untrusted"


@pytest.mark.parametrize("field,status", [
    ("subject_binding","unverified"),
    ("organizational_binding","revoked"),
    ("authority_to_bind","contradictory"),
    ("authority_to_bind","indeterminate"),
])
def test_partial_or_conflicting_claims_cannot_elevate(field,status):
    claims = dict(CLAIMS)
    claims[field] = status
    outcome = assess_signer_binding({"proof":"verified"}, claims)
    assert outcome["assured_authority"] == "indeterminate"
    assert outcome["organizational_revocation"] == "not_checked"


def test_tampered_and_unknown_key_non_positive():
    changed = signed()
    changed["statement"]["resources"] = ["post:other"]
    invalid = verify_statement(changed, {"fixture:enterprise": PUB})
    assert invalid["proof"] == "invalid"
    assert assess_signer_binding(invalid, CLAIMS)["reason"] == "statement_integrity_invalid"
    missing = verify_statement(signed(), {})
    assert missing["proof"] == "indeterminate"
    assert assess_signer_binding(missing, CLAIMS)["reason"] == "statement_integrity_indeterminate"


@pytest.mark.parametrize("claims", [
    {},
    {"subject_binding":"verified","organizational_binding":"verified","authority_to_bind":True},
    {"subject_binding":"verified","organizational_binding":"authorized","authority_to_bind":"verified"},
])
def test_invalid_binding_evidence_is_rejected(claims):
    with pytest.raises(ValueError):
        assess_signer_binding({"proof":"verified"}, claims)
