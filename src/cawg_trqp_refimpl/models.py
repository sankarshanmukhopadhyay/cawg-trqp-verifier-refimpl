from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class VerificationRequest:
    asset_id: str
    integrity_ok: bool
    entity_id: str
    authority_id: str
    issuer_id: str | None
    action: str
    resource: str
    context: dict[str, Any] = field(default_factory=dict)
    process_evidence: dict[str, Any] | None = None


@dataclass
class AuthorizationResponse:
    authorized: bool
    expires: str | None = None
    policy_epoch: str | None = None
    evidence: list[str] = field(default_factory=list)
    reason: str | None = None
    policy_requirements: dict[str, Any] = field(default_factory=dict)


@dataclass
class RecognitionResponse:
    recognized: bool
    expires: str | None = None
    policy_epoch: str | None = None
    evidence: list[str] = field(default_factory=list)
    reason: str | None = None


@dataclass
class VerificationResult:
    asset_integrity: str
    assertion_binding: str
    issuer_recognition: str
    actor_authorization: str
    process_integrity: str
    policy_freshness: str
    verification_mode: str
    trust_outcome: str
    process_appraisal: dict[str, Any] = field(default_factory=dict)
    explanations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
