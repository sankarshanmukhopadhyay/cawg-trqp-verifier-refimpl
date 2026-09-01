from __future__ import annotations
from dataclasses import dataclass, field, asdict
import math
from numbers import Real
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

    def __post_init__(self) -> None:
        """Enforce the typed verifier contract at request construction time.

        HTTP construction occurs inside the service's invalid-request boundary, so
        these ValueErrors become deterministic 400 responses rather than failures
        during assurance evaluation. Direct library consumers receive the same
        contract rather than a weaker one.
        """
        if not isinstance(self.context, dict):
            raise ValueError("context must be a JSON object")
        if self.process_evidence is None:
            return
        if not isinstance(self.process_evidence, dict):
            raise ValueError("process_evidence must be a JSON object or null")

        evidence = self.process_evidence
        if "confidence" in evidence:
            confidence = evidence["confidence"]
            if isinstance(confidence, bool) or not isinstance(confidence, Real):
                raise ValueError("process_evidence.confidence must be a finite number between 0 and 1")
            numeric_confidence = float(confidence)
            if not math.isfinite(numeric_confidence) or not 0.0 <= numeric_confidence <= 1.0:
                raise ValueError("process_evidence.confidence must be a finite number between 0 and 1")

        for field_name in ("process_type", "evidence_ref", "evidence_format", "appraisal", "reference"):
            if field_name in evidence and evidence[field_name] is not None:
                value = evidence[field_name]
                if not isinstance(value, str) or not value:
                    raise ValueError(f"process_evidence.{field_name} must be a non-empty string when supplied")

        if "verified" in evidence and not isinstance(evidence["verified"], bool):
            raise ValueError("process_evidence.verified must be a boolean when supplied")


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
    policy_evidence: dict[str, Any] = field(default_factory=dict)
    gateway_mediation: dict[str, Any] = field(default_factory=dict)
    assertion_evaluation: dict[str, Any] = field(default_factory=dict)
    conflict_evaluation: dict[str, Any] = field(default_factory=dict)
    propositions: dict[str, Any] = field(default_factory=dict)
    explanations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
