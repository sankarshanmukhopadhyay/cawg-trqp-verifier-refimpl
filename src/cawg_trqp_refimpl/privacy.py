from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PrivacyProfile:
    id: str
    include_raw_request: bool
    include_process_evidence: bool
    pseudonymize_identifiers: bool
    retention_days: int
    access_scope: str


BUILTIN_PRIVACY_PROFILES = {
    "minimal_receipt": PrivacyProfile(
        id="minimal_receipt", include_raw_request=False, include_process_evidence=False,
        pseudonymize_identifiers=True, retention_days=30, access_scope="trqp.receipt.read"
    ),
    "replay_bundle": PrivacyProfile(
        id="replay_bundle", include_raw_request=True, include_process_evidence=True,
        pseudonymize_identifiers=False, retention_days=90, access_scope="trqp.audit.export"
    ),
    "regulated_evidence": PrivacyProfile(
        id="regulated_evidence", include_raw_request=True, include_process_evidence=True,
        pseudonymize_identifiers=False, retention_days=365, access_scope="trqp.audit.regulated"
    ),
}


def load_privacy_profile(value: str | PrivacyProfile | None) -> PrivacyProfile:
    if isinstance(value, PrivacyProfile):
        return value
    key = value or "minimal_receipt"
    try:
        return BUILTIN_PRIVACY_PROFILES[key]
    except KeyError as exc:
        raise ValueError(f"unknown privacy profile: {key}") from exc


def validate_context(context: dict[str, Any], allowed_fields: set[str] | None = None) -> None:
    if allowed_fields is None:
        return
    unexpected = sorted(set(context) - allowed_fields)
    if unexpected:
        raise ValueError(f"context contains fields not allowed by the active context profile: {', '.join(unexpected)}")
