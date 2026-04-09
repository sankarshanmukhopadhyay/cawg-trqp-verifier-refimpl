from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .jsoncanon import canonical_json_bytes, sha256_hex
from .models import VerificationRequest, VerificationResult
from .profile import VerificationProfile, load_profile

AUDIT_BUNDLE_TYPE = "cawg-trqp-audit-bundle"
AUDIT_BUNDLE_PROFILE = "https://example.org/profiles/cawg-trqp-audit-bundle/v1"
AUDIT_BUNDLE_VERSION = "1.2.0"


@dataclass
class AuditBundle:
    bundle_type: str
    bundle_profile: str
    bundle_version: str
    exported_at: str
    bundle_id: str
    bundle_digest_sha256: str
    request_summary: dict[str, Any]
    verification_result: dict[str, Any]
    policy_evidence: dict[str, Any]
    process_appraisal: dict[str, Any]
    gateway_mediation: dict[str, Any] = field(default_factory=dict)
    replay_inputs: dict[str, Any] = field(default_factory=dict)
    bundle_attestation: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content = {
            "bundle_type": self.bundle_type,
            "bundle_profile": self.bundle_profile,
            "bundle_version": self.bundle_version,
            "exported_at": self.exported_at,
            "bundle_id": self.bundle_id,
            "request_summary": self.request_summary,
            "verification_result": self.verification_result,
            "policy_evidence": self.policy_evidence,
            "process_appraisal": self.process_appraisal,
            "gateway_mediation": self.gateway_mediation,
            "replay_inputs": self.replay_inputs,
        }
        content["bundle_digest_sha256"] = sha256_hex(content)
        if self.bundle_attestation:
            content["bundle_attestation"] = self.bundle_attestation
        return content

    def to_canonical_json(self) -> bytes:
        return canonical_json_bytes(self.to_dict())



def _request_to_summary(request: VerificationRequest) -> dict[str, Any]:
    return {
        "asset_id": request.asset_id,
        "entity_id": request.entity_id,
        "authority_id": request.authority_id,
        "issuer_id": request.issuer_id,
        "action": request.action,
        "resource": request.resource,
        "context": request.context,
        "has_process_evidence": request.process_evidence is not None,
    }



def build_audit_bundle(
    request: VerificationRequest,
    result: VerificationResult,
    *,
    profile: str | dict[str, Any] | VerificationProfile = "standard",
    use_gateway: bool = False,
    exported_at: str | None = None,
    policy_path: str | Path | None = None,
    revocation_path: str | Path | None = None,
) -> AuditBundle:
    resolved_profile = load_profile(profile)
    controls = resolved_profile.controls
    if controls["determinism"]["require_pinned_feeds"] and policy_path is None:
        raise ValueError("profile requires pinned policy feeds for deterministic replay")

    exported_at = exported_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    request_summary = _request_to_summary(request)
    policy_feed = {}
    if policy_path is not None:
        policy_feed["policy_source"] = str(policy_path)
        policy_feed["policy_source_sha256"] = sha256_hex(Path(policy_path).read_text(encoding="utf-8"))
    if revocation_path is not None:
        policy_feed["revocation_source"] = str(revocation_path)
        policy_feed["revocation_source_sha256"] = sha256_hex(Path(revocation_path).read_text(encoding="utf-8"))

    replay_inputs = {
        "request": {
            "asset_id": request.asset_id,
            "integrity_ok": request.integrity_ok,
            "entity_id": request.entity_id,
            "authority_id": request.authority_id,
            "issuer_id": request.issuer_id,
            "action": request.action,
            "resource": request.resource,
            "context": request.context,
            "process_evidence": request.process_evidence,
        },
        "profile": resolved_profile.to_dict(),
        "use_gateway": use_gateway,
        "verification_mode": result.verification_mode,
        "policy_epoch": result.policy_evidence.get("policy_epoch"),
    }
    if policy_feed:
        replay_inputs["policy_feed"] = policy_feed
    bundle_seed = {
        "request_summary": request_summary,
        "verification_result": result.to_dict(),
        "policy_evidence": result.policy_evidence,
        "process_appraisal": result.process_appraisal,
        "gateway_mediation": result.gateway_mediation,
        "replay_inputs": replay_inputs,
    }
    bundle_id = f"urn:trqp:audit-bundle:sha256:{sha256_hex(bundle_seed)}"
    bundle = AuditBundle(
        bundle_type=AUDIT_BUNDLE_TYPE,
        bundle_profile=AUDIT_BUNDLE_PROFILE,
        bundle_version=AUDIT_BUNDLE_VERSION,
        exported_at=exported_at,
        bundle_id=bundle_id,
        bundle_digest_sha256="",
        request_summary=request_summary,
        verification_result=result.to_dict(),
        policy_evidence=result.policy_evidence,
        process_appraisal=result.process_appraisal,
        gateway_mediation=result.gateway_mediation,
        replay_inputs=replay_inputs,
    )
    bundle.bundle_digest_sha256 = bundle.to_dict()["bundle_digest_sha256"]
    return bundle
