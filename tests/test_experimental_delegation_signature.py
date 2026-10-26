"""Cryptographic integration tests with deterministic, non-production test keys."""
import base64
import copy
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cawg_trqp_refimpl.experimental_delegation_signature import canonical_bytes, verify_statement

# Publicly reproducible fixture key. NEVER use in a live trust registry.
PRIVATE = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
PUBLIC = PRIVATE.public_key().public_bytes(
    encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
STMT={"delegator":"publisher","delegate":"freelancer","actions":["publish"],
      "resources":["article:1"],"purposes":["news"],
      "not_before":"2026-10-01T00:00:00Z","not_after":"2026-10-31T00:00:00Z"}
def envelope(statement=None):
    statement=copy.deepcopy(statement if statement is not None else STMT)
    return {"statement":statement,"key_id":"fixture:publisher",
            "signature_b64":base64.b64encode(PRIVATE.sign(canonical_bytes(statement))).decode()}

def test_pinned_public_key_checks_actual_signature():
    result=verify_statement(envelope(),{"fixture:publisher":PUBLIC})
    assert result["proof"]=="verified"
    assert result["issuer_trust"]=="not_evaluated"
    assert result["trusted_signing_time"]=="not_evaluated"
    assert result["c2pa_binding"]=="not_evaluated"
    assert result["assurance_scope"]=="statement_integrity_only"

def test_tampering_fails_and_does_not_establish_authority():
    signed=envelope()
    for name,mutation in [
        ("scope",lambda x:x["statement"]["resources"].append("article:2")),
        ("period",lambda x:x["statement"].update(not_after="2026-12-01T00:00:00Z")),
        ("actor",lambda x:x["statement"].update(delegate="impostor")),
        ("signature",lambda x:x.update(signature_b64=base64.b64encode(b"0"*64).decode())),
    ]:
        case=copy.deepcopy(signed)
        mutation(case)
        assert verify_statement(case,{"fixture:publisher":PUBLIC})["proof"]=="invalid",name

def test_unknown_key_is_indeterminate_not_positive():
    r=verify_statement(envelope(),{})
    assert r=={"proof":"indeterminate","reason":"key_unrecognized"}

def test_wrong_anchor_rejects_signature():
    other=Ed25519PrivateKey.from_private_bytes(bytes(reversed(range(32))))
    key=other.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
    assert verify_statement(envelope(),{"fixture:publisher":key})["proof"]=="invalid"

def test_malformed_evidence_never_verifies():
    e=envelope()
    e["signature_b64"]="not-b64!"
    assert verify_statement(e,{"fixture:publisher":PUBLIC})["proof"]=="invalid"
    e=envelope()
    e["statement"]["not_after"]=None
    assert verify_statement(e,{"fixture:publisher":PUBLIC})["proof"]=="invalid"

def test_reproducible_signature_bytes():
    assert envelope()["signature_b64"]==envelope()["signature_b64"]
