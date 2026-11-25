"""Compose local proof, scope and consent assessments without trust elevation.

This is a single-edge experimental consumer path, not a CAWG wire profile,
a TRQP transport, an authorization grant or a legal determination.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime

from .experimental_consent_assurance import assess_consent
from .experimental_subject_evidence import assess_subject_evidence
from .experimental_two_party_delegation import signing_bytes, verify_two_party
from .experimental_source_evidence import assess_signed_claim, outcome
from .jsoncanon import canonical_json_bytes

_SOURCE_KINDS = {
    "delegator_binding": "subject-key-binding",
    "delegate_binding": "subject-key-binding",
    "authority_to_delegate": "authority-to-delegate",
    "delegation_status": "delegation-status",
    "consent_record": "consent-record",
}

_REQUEST_FIELDS = {
    "principal", "actor", "action", "resource", "purpose",
    "used_at", "evaluated_at", "context_sha256", "consent_subject",
}


def _timestamp(value):
    if not isinstance(value, str):
        raise ValueError("timestamp_invalid")
    time = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if time.utcoffset() is None:
        raise ValueError("timestamp_unzoned")
    return time


def assess_operation(request, envelope, pinned_keys, *, consent_records=None,
                     subject_evidence=None, source_packages=None, source_policies=None,
                     source_observed_at=None):
    """Assess supplied evidence relative to a separately supplied operation.

    Times and context are caller-supplied, not trusted timestamp/manifest
    evidence. No network I/O, legal identity resolution or authority promotion.
    """
    result = {
        "profile": "experimental-taskforce-operation/0.1",
        "request_status": "invalid",
        "statement_integrity": "not_checked",
        "delegation_at_use": "indeterminate",
        "delegation_current": "indeterminate",
        "subject_binding": "indeterminate",
        "subject_evidence_status": "not_checked",
        "consent_evidence_status": "not_checked",
        "consent_at_use": "indeterminate",
        "consent_current": "indeterminate",
        "assured_authority": "indeterminate",
        "assured_consent": "indeterminate",
        "guardian_authority": "not_checked",
        "witness_authority": "not_checked",
        "registry_recognition": "not_checked",
        "delegation_status_evidence": "not_checked",
        "trusted_time": "not_checked",
        "c2pa_binding": "not_checked",
        "source_evidence": {name: outcome("not_checked", "source_not_supplied")
                            for name in _SOURCE_KINDS},
        "reason": "request_invalid",
    }
    try:
        if not isinstance(request, dict) or set(request) != _REQUEST_FIELDS:
            return result
        for field in ("principal", "actor", "action", "resource", "purpose"):
            if not isinstance(request[field], str) or not request[field].strip():
                return result
        subject = request["consent_subject"]
        if subject is not None and (not isinstance(subject, str) or not subject.strip()):
            return result
        digest = request["context_sha256"]
        if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
            return result
        used, now = _timestamp(request["used_at"]), _timestamp(request["evaluated_at"])
        if now < used:
            return result
    except (ValueError, TypeError, OverflowError):
        return result

    result.update(request_status="valid", reason="independent_evidence_required")
    expected_claims = {}
    proof = verify_two_party(envelope, pinned_keys, expected_context_sha256=digest)
    result["statement_integrity"] = proof["statement_integrity"]
    if proof["statement_integrity"] == "verified":
        terms = envelope["statement"]
        matches = (terms["delegator"] == request["principal"]
                   and terms["delegate"] == request["actor"]
                   and request["action"] in terms["actions"]
                   and request["resource"] in terms["resources"]
                   and request["purpose"] in terms["purposes"])
        start, end = _timestamp(terms["not_before"]), _timestamp(terms["not_after"])
        if matches:
            signer_ids = {role: envelope["signatures"][role]["key_id"]
                          for role in ("delegator", "delegate")}
            hashes = {role: hashlib.sha256(pinned_keys[key_id]).hexdigest()
                      for role, key_id in signer_ids.items()}
            for role, subject_field in (("delegator", "principal"), ("delegate", "actor")):
                expected_claims[role + "_binding"] = {
                    "subject_ref": request[subject_field], "key_sha256": hashes[role]}
            signed_terms = {
                "statement_sha256": hashlib.sha256(signing_bytes(
                    terms, digest, "delegator", signer_ids["delegator"])).hexdigest(),
                "delegator_key_sha256": hashes["delegator"],
                "delegate_key_sha256": hashes["delegate"],
            }
            expected_claims["authority_to_delegate"] = signed_terms
            expected_claims["delegation_status"] = signed_terms
        result["delegation_at_use"] = (
            "signed_terms_in_scope" if matches and start <= used < end
            else "signed_terms_out_of_scope"
        )
        result["delegation_current"] = (
            "signed_terms_in_scope" if matches and start <= now < end
            else "signed_terms_out_of_scope"
        )
    else:
        result["reason"] = proof["reason"]

    # Subject evidence concerns the actor, not necessarily the person consenting.
    if subject_evidence is not None:
        try:
            assessment = assess_subject_evidence(subject_evidence)
            if subject_evidence["subject"] != request["actor"]:
                result["subject_evidence_status"] = "subject_mismatch"
            else:
                result["subject_evidence_status"] = assessment["evidence_origin"]
        except (ValueError, TypeError, KeyError):
            result["subject_evidence_status"] = "invalid"

    # Evaluate the separate consent proposition even if delegation fails.
    # A missing subject is not proof that consent is unnecessary.
    if subject is not None:
        try:
            consent = assess_consent({
                "case_id": "local-operation",
                "subject_ref": subject,
                "action": request["action"], "resource": request["resource"],
                "purpose": request["purpose"], "used_at": request["used_at"],
                "evaluated_at": request["evaluated_at"],
                "records": [] if consent_records is None else consent_records,
            })
            result.update(
                consent_evidence_status=consent["consent_evidence_status"],
                consent_at_use=consent["consent_at_use_time"],
                consent_current=consent["consent_current_state"],
            )
            if consent["consent_evidence_status"] == "unverified":
                matching = [record for record in (consent_records or [])
                            if record["subject_ref"] == subject
                            and request["action"] in record["actions"]
                            and request["resource"] in record["resources"]
                            and request["purpose"] in record["purposes"]]
                if len(matching) == 1:
                    expected_claims["consent_record"] = {
                        "subject_ref": subject,
                        "record_sha256": hashlib.sha256(
                            canonical_json_bytes(matching[0])).hexdigest(),
                    }
        except (ValueError, TypeError, KeyError, OverflowError):
            result["consent_evidence_status"] = "invalid"
    elif consent_records is not None and consent_records != []:
        result["consent_evidence_status"] = "subject_missing"

    # Source packages are opt-in and already locally available. The relying
    # party must configure sources and its observation clock separately.
    if source_packages is not None or source_policies is not None:
        packages = {} if source_packages is None else source_packages
        policies = {} if source_policies is None else source_policies
        if (not isinstance(packages, dict) or not isinstance(policies, dict)
                or not set(packages) <= set(_SOURCE_KINDS)
                or not set(policies) <= set(_SOURCE_KINDS)):
            result["source_evidence"] = {
                name: outcome("invalid", "source_inputs_invalid") for name in _SOURCE_KINDS}
        else:
            for name, kind in _SOURCE_KINDS.items():
                if name not in packages and name not in policies:
                    continue
                if name not in expected_claims:
                    result["source_evidence"][name] = outcome(
                        "indeterminate", "matching_operation_claim_unavailable")
                elif source_observed_at != now:
                    result["source_evidence"][name] = outcome(
                        "indeterminate", "source_clock_mismatch_or_unavailable")
                else:
                    result["source_evidence"][name] = assess_signed_claim(
                        packages.get(name), policies.get(name), kind=kind,
                        expected_claim=expected_claims[name], observed_at=source_observed_at)

    # Explicit allowlist above: no request IDs, raw terms, keys, references,
    # registry assertions or private record content in the public result.
    return result
