"""Experimental subject/vouching evidence classification, NOT identity proof.

Caller-submitted assertions can be described but never upgrade assured identity,
uniqueness or authorization. Neither a professional licence nor uniqueness
claims are delegation evidence. No network fetches or credential verification.
"""
from __future__ import annotations

from typing import Any

SUBJECT_KINDS = frozenset({"self-declared", "pseudonymous", "identified"})
VOUCHING_KINDS = frozenset({"peer", "platform", "professional", "public", "organization"})
STATES = frozenset({"unverified", "indeterminate", "verified", "contradictory", "revoked"})


def assess_subject_evidence(statement: dict[str, Any]) -> dict[str, Any]:
    """Produce a non-authoritative assessment of *claims*, not a grant.

    This function has no trusted issuer/identity/uniqueness verification inputs.
    The caller's claimed verification status is retained only as an untrusted
    assertion, never as the assured status.
    """
    if not isinstance(statement, dict) or set(statement) != {
        "subject", "kind", "unique_claim", "vouching"
    }:
        raise ValueError("subject_statement_invalid")
    subject = statement["subject"]
    if not isinstance(subject, str) or not subject.strip() or len(subject) > 256:
        raise ValueError("subject_reference_invalid")
    if statement["kind"] not in SUBJECT_KINDS:
        raise ValueError("subject_kind_invalid")
    if not isinstance(statement["unique_claim"], bool):
        raise ValueError("unique_claim_invalid")
    vouching = statement["vouching"]
    if not isinstance(vouching, list) or len(vouching) > 16:
        raise ValueError("vouching_invalid")
    sources = []
    for item in vouching:
        if not isinstance(item, dict) or set(item) != {
            "issuer", "kind", "claimed_status", "scope"
        }:
            raise ValueError("vouching_entry_invalid")
        if (not isinstance(item["issuer"], str) or not item["issuer"].strip()
                or len(item["issuer"]) > 256
                or item["kind"] not in VOUCHING_KINDS
                or item["claimed_status"] not in STATES
                or not isinstance(item["scope"], str)
                or not item["scope"].strip() or len(item["scope"]) > 256):
            raise ValueError("vouching_entry_invalid")
        sources.append({
            "kind": item["kind"],
            "claimed_status": item["claimed_status"],
            "verification": "not_checked",
            "recognition": "not_checked",
            "revocation": "not_checked",
        })
    return {
        "profile": "experimental-subject-evidence/0.1",
        "subject_kind": statement["kind"],
        "self_declaration": True,
        "unique_claim_present": statement["unique_claim"],
        "assured_uniqueness": "indeterminate",
        "assured_subject_binding": "indeterminate",
        "assured_vouching": "unverified",
        "assured_authority": "indeterminate",
        "evidence_origin": "caller_supplied_simulation",
        "vouching_sources": sources,
        "reason": "independent_subject_and_issuer_evidence_unavailable",
    }
