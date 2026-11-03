"""Separate Ed25519 statement integrity from external enterprise authority.

This module has no trusted subject-to-key, enterprise, authority, or historical
revocation resolver. Claimed relationships cannot become assured outcomes.
"""
from __future__ import annotations

from typing import Any

INTEGRITY = frozenset({"verified", "invalid", "indeterminate"})
CLAIM_STATES = frozenset({"verified", "unverified", "indeterminate", "revoked", "contradictory"})


def assess_signer_binding(signature_result: dict[str, Any],
                          claims: dict[str, Any]) -> dict[str, Any]:
    """Classify untrusted external claims without elevating authorization.

    signature_result must be the output of the local experimental signature
    verifier; its verified status covers statement integrity only. No caller-
    supplied enterprise/authority flags are treated as verified evidence.
    """
    if not isinstance(signature_result, dict) or signature_result.get("proof") not in INTEGRITY:
        raise ValueError("signature_result_invalid")
    if not isinstance(claims, dict) or set(claims) != {
        "subject_binding", "organizational_binding", "authority_to_bind"
    } or any(value not in CLAIM_STATES for value in claims.values()):
        raise ValueError("binding_claims_invalid")
    integrity = signature_result["proof"]
    # A valid signature proves only statement integrity, never who owns the key.
    result = {
        "profile": "experimental-signer-binding/0.1",
        "statement_integrity": integrity,
        "subject_binding": "indeterminate",
        "organizational_binding": "indeterminate",
        "authority_to_bind": "indeterminate",
        "delegated_authority": "indeterminate",
        "assured_authority": "indeterminate",
        "claim_provenance": "caller_supplied_untrusted",
        "claimed_relationships": dict(claims),
        "trusted_signing_time": "not_checked",
        "organizational_revocation": "not_checked",
        "reason": "external_binding_evidence_not_verified",
    }
    if integrity == "invalid":
        result["reason"] = "statement_integrity_invalid"
    elif integrity == "indeterminate":
        result["reason"] = "statement_integrity_indeterminate"
    return result
