"""Repository-local consent evidence assessment, not consent or legal verification.

All asserted consent states, times and evidence references are supplied by the
caller. No credential, issuer, signer, registry or historical state is trusted.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

PROFILE = "experimental-consent-assurance/0.1"


class InvalidConsentCase(ValueError):
    """Input does not satisfy the experimental consent case contract."""


def _time(value: Any) -> datetime:
    if not isinstance(value, str):
        raise InvalidConsentCase("timestamp_invalid")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise InvalidConsentCase("timestamp_invalid") from exc
    if parsed.utcoffset() is None:
        raise InvalidConsentCase("timestamp_unzoned")
    return parsed.astimezone(timezone.utc)


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidConsentCase(label + "_invalid")
    return value


def _scope(value: Any, label: str) -> set[str]:
    if not isinstance(value, list) or not value or any(
        not isinstance(v, str) or not v.strip() for v in value
    ) or len(value) != len(set(value)):
        raise InvalidConsentCase(label + "_invalid")
    return set(value)


def assess_consent(case: dict[str, Any]) -> dict[str, Any]:
    """Assess claims and uncertainty without implying authentic permission."""
    required = {"case_id", "subject_ref", "action", "resource", "purpose",
                "used_at", "evaluated_at", "records"}
    if not isinstance(case, dict) or set(case) != required:
        raise InvalidConsentCase("case_fields_invalid")
    for key in ("case_id", "subject_ref", "action", "resource", "purpose"):
        _text(case[key], key)
    used, now = _time(case["used_at"]), _time(case["evaluated_at"])
    records = case["records"]
    if not isinstance(records, list) or len(records) > 32:
        raise InvalidConsentCase("records_invalid")
    result = {
        "profile": PROFILE, "case_id": case["case_id"],
        "consent_evidence_status": "missing" if not records else "unverified",
        "consent_scope_status": "indeterminate",
        "consent_at_use_time": "indeterminate",
        "consent_current_state": "indeterminate",
        "assured_consent": "indeterminate",
        "consent_time_provenance": "caller_supplied_untrusted",
        "consent_source_provenance": "caller_supplied_unverified",
        "reason": "consent_evidence_missing" if not records else "consent_not_established",
    }
    if not records:
        return result
    seen: dict[str, dict[str, Any]] = {}
    parsed = []
    fields = {"record_id", "subject_ref", "actions", "resources", "purposes",
              "valid_from", "valid_until", "withdrawn_effective_at",
              "withdrawal_observed_at", "evidence_ref", "evidence_sha256"}
    for record in records:
        if not isinstance(record, dict) or set(record) != fields:
            raise InvalidConsentCase("record_fields_invalid")
        rid = _text(record["record_id"], "record_id")
        _text(record["subject_ref"], "subject_ref")
        start, end = _time(record["valid_from"]), _time(record["valid_until"])
        if start >= end:
            raise InvalidConsentCase("record_interval_invalid")
        withdrawn = record["withdrawn_effective_at"]
        observed = record["withdrawal_observed_at"]
        if (withdrawn is None) != (observed is None):
            raise InvalidConsentCase("withdrawal_provenance_incomplete")
        withdrawal_time = _time(withdrawn) if withdrawn is not None else None
        if observed is not None:
            _time(observed)
        uri = _text(record["evidence_ref"], "evidence_ref")
        if not uri.startswith("https://"):
            raise InvalidConsentCase("evidence_ref_invalid")
        digest = record["evidence_sha256"]
        if not isinstance(digest, str) or re.fullmatch(r"[a-fA-F0-9]{64}", digest) is None:
            raise InvalidConsentCase("evidence_digest_invalid")
        actions = _scope(record["actions"], "actions")
        resources = _scope(record["resources"], "resources")
        purposes = _scope(record["purposes"], "purposes")
        if rid in seen:
            result["consent_evidence_status"] = "contradictory"
            result["reason"] = "duplicate_consent_record"
            return result
        seen[rid] = record
        parsed.append((record, actions, resources, purposes, start, end, withdrawal_time))
    matches = [p for p in parsed if p[0]["subject_ref"] == case["subject_ref"]
               and case["action"] in p[1] and case["resource"] in p[2]
               and case["purpose"] in p[3]]
    if not matches:
        result.update(consent_scope_status="outside_claimed_scope",
                      consent_at_use_time="claimed_out_of_scope",
                      reason="no_matching_consent_scope")
        return result
    result["consent_scope_status"] = "within_claimed_scope"
    # An ambiguous set of overlapping evidence claims cannot be silently selected.
    if len(matches) != 1:
        result.update(consent_evidence_status="contradictory",
                      reason="multiple_matching_consent_records")
        return result
    record, _, _, _, start, end, withdrawn = matches[0]
    if not start <= used < end:
        result.update(consent_at_use_time="claimed_out_of_scope",
                      reason="outside_claimed_consent_interval")
    elif withdrawn is not None and withdrawn <= used:
        result.update(consent_at_use_time="claimed_out_of_scope",
                      reason="claimed_withdrawal_before_use")
    else:
        result.update(consent_at_use_time="claimed_in_scope",
                      reason="within_unverified_claimed_consent_scope")
    # A withdrawal observed after the evaluation time must not be presented
    # as an observed current state, even if it claims an earlier effective date.
    observed = _time(record["withdrawal_observed_at"]) if withdrawn is not None else None
    if withdrawn is not None and withdrawn <= now and observed > now:
        result["consent_current_state"] = "indeterminate"
        result["reason"] = "withdrawal_not_observed_as_of_evaluation"
    elif withdrawn is not None and withdrawn <= now:
        result["consent_current_state"] = "claimed_withdrawn"
    elif not start <= now < end:
        result["consent_current_state"] = "claimed_expired"
    else:
        result["consent_current_state"] = "claimed_active"
    return result
