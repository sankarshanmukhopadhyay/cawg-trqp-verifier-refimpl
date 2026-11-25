"""Local two-party delegation integrity experiment, not a CAWG credential format.

Both role-bound signatures cover the same statement and context. Pinned keys
are verification inputs, not proof of identity, recognition or authority.
No network access or consent inference is performed.
"""
from __future__ import annotations

import base64
import json
import re
from datetime import datetime

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .experimental_delegation_signature import canonical_bytes

DOMAIN = b"CAWG-TRQP-EXPERIMENTAL-TWO-PARTY-V1\x00"
ROLES = ("delegator", "delegate")


def signing_bytes(statement, context, role, key_id):
    """Bind role, key identifier, terms and context digest to each signature."""
    if role not in ROLES or not isinstance(key_id, str) or not key_id:
        raise ValueError("signer_invalid")
    canonical_bytes(statement)  # Reuse the existing statement shape contract.
    if statement["delegator"] == statement["delegate"]:
        raise ValueError("parties_not_distinct")
    for field in ("actions", "resources", "purposes"):
        if len(set(statement[field])) != len(statement[field]):
            raise ValueError("duplicate_scope")
    start, end = (datetime.fromisoformat(statement[f].replace("Z", "+00:00"))
                  for f in ("not_before", "not_after"))
    if start.utcoffset() is None or end.utcoffset() is None or start >= end:
        raise ValueError("interval_invalid")
    if not isinstance(context, str) or not re.fullmatch(r"[0-9a-f]{64}", context):
        raise ValueError("context_digest_invalid")
    return DOMAIN + json.dumps(
        {"statement": statement, "context_sha256": context,
         "role": role, "key_id": key_id},
        sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False,
    ).encode("utf-8")


def verify_two_party(envelope, pinned_keys, *, expected_context_sha256):
    """Assess signatures over caller-supplied context, not actual C2PA coverage.

    No caller-provided trust or consent Boolean can elevate the result.
    Public output deliberately omits subject identifiers and private terms.
    """
    result = {
        "profile": "experimental-two-party-delegation/0.1",
        "statement_integrity": "indeterminate",
        "delegator_binding": "indeterminate",
        "delegate_binding": "indeterminate",
        "assured_authority": "indeterminate",
        "assured_consent": "indeterminate",
        "trusted_signing_time": "not_checked",
        "status_evidence": "not_checked",
        "c2pa_binding": "not_checked",
        "reason": "evidence_unavailable",
    }

    def finish(state, reason):
        return dict(result, statement_integrity=state, reason=reason)

    try:
        if not isinstance(envelope, dict) or set(envelope) != {
            "statement", "context_sha256", "signatures"
        } or not isinstance(pinned_keys, dict):
            return finish("invalid", "envelope_malformed")
        context = envelope["context_sha256"]
        if context != expected_context_sha256:
            return finish("invalid", "context_mismatch")
        signatures = envelope["signatures"]
        if not isinstance(signatures, dict) or set(signatures) != set(ROLES):
            return finish("invalid", "signer_roles_invalid")
        keys = []
        missing = False
        for role in ROLES:
            signer = signatures[role]
            if not isinstance(signer, dict) or set(signer) != {"key_id", "signature_b64"}:
                return finish("invalid", "signer_malformed")
            key_id = signer["key_id"]
            payload = signing_bytes(envelope["statement"], context, role, key_id)
            encoded = signer["signature_b64"]
            if not isinstance(encoded, str):
                raise ValueError("signature_encoding")
            signature = base64.b64decode(encoded, validate=True)
            if len(signature) != 64:
                raise ValueError("signature_length")
            key = pinned_keys.get(key_id)
            keys.append((key_id, key))
            if not isinstance(key, bytes) or len(key) != 32:
                missing = True
                continue
            Ed25519PublicKey.from_public_bytes(key).verify(signature, payload)
        if keys[0][0] == keys[1][0] or (
            not missing and keys[0][1] == keys[1][1]
        ):
            return finish("invalid", "signer_keys_not_distinct")
        if missing:
            return finish("indeterminate", "key_unrecognized")
    except (ValueError, TypeError, KeyError, InvalidSignature, OverflowError):
        return finish("invalid", "signature_or_statement_invalid")
    return finish("verified", "integrity_only_external_authority_unverified")
