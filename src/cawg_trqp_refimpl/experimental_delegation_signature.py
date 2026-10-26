"""Experimental Ed25519 delegation statement verification.

Key anchoring is caller-supplied and never means CAWG/C2PA issuer recognition.
Signatures are over canonical JSON bytes with a fixed domain separator. This is
NOT a CAWG identity assertion, C2PA signature, trusted timestamp or TRQP query.
"""
from __future__ import annotations
import base64
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DOMAIN = b"CAWG-TRQP-EXPERIMENTAL-DELEGATION-V1\x00"

def canonical_bytes(statement):
    if not isinstance(statement, dict):
        raise ValueError("statement_malformed")
    required={"delegator","delegate","actions","resources","purposes","not_before","not_after"}
    if set(statement)!=required:
        raise ValueError("statement_fields_invalid")
    for k in ("delegator","delegate","not_before","not_after"):
        if not isinstance(statement[k],str) or not statement[k]:
            raise ValueError("statement_fields_invalid")
    for k in ("actions","resources","purposes"):
        values=statement[k]
        if not isinstance(values,list) or not values or any(not isinstance(v,str) or not v for v in values):
            raise ValueError("statement_fields_invalid")
    return DOMAIN+json.dumps(statement,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()

def verify_statement(envelope, trusted_keys):
    """Return a bounded proof result, not an authorization or issuer-trust verdict."""
    if not isinstance(envelope,dict) or set(envelope)!={"statement","key_id","signature_b64"}:
        return {"proof":"invalid","reason":"envelope_malformed"}
    key_id=envelope["key_id"]
    if not isinstance(key_id,str) or not isinstance(trusted_keys,dict):
        return {"proof":"invalid","reason":"key_unrecognized"}
    key_bytes=trusted_keys.get(key_id)
    if not isinstance(key_bytes,bytes) or len(key_bytes)!=32:
        return {"proof":"indeterminate","reason":"key_unrecognized"}
    try:
        payload=canonical_bytes(envelope["statement"])
        encoded=envelope["signature_b64"]
        if not isinstance(encoded,str):
            raise ValueError("signature_encoding")
        signature=base64.b64decode(encoded,validate=True)
        if len(signature)!=64:
            raise ValueError("signature_length")
        Ed25519PublicKey.from_public_bytes(key_bytes).verify(signature,payload)
    except (ValueError,TypeError,InvalidSignature):
        return {"proof":"invalid","reason":"signature_or_statement_invalid"}
    return {"proof":"verified","reason":"ed25519_signature_valid",
            "assurance_scope":"statement_integrity_only",
            "issuer_trust":"not_evaluated",
            "trusted_signing_time":"not_evaluated",
            "c2pa_binding":"not_evaluated"}
