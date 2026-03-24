from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any

from .models import VerificationRequest, VerificationResult


@dataclass
class AuditBundle:
    bundle_type: str
    bundle_version: str
    exported_at: str
    request_summary: dict[str, Any]
    verification_result: dict[str, Any]
    policy_evidence: dict[str, Any]
    process_appraisal: dict[str, Any]
    gateway_mediation: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_audit_bundle(request: VerificationRequest, result: VerificationResult) -> AuditBundle:
    return AuditBundle(
        bundle_type='cawg-trqp-audit-bundle',
        bundle_version='0.9.0',
        exported_at=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        request_summary={
            'asset_id': request.asset_id,
            'entity_id': request.entity_id,
            'authority_id': request.authority_id,
            'issuer_id': request.issuer_id,
            'action': request.action,
            'resource': request.resource,
            'context': request.context,
            'has_process_evidence': request.process_evidence is not None,
        },
        verification_result=result.to_dict(),
        policy_evidence=result.policy_evidence,
        process_appraisal=result.process_appraisal,
        gateway_mediation=result.gateway_mediation,
    )
