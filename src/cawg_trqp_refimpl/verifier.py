"""CAWG–TRQP verifier orchestrating trust decisions across online, cached, and offline modes."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Optional, Any

from .cache import TTLCache
from .context import tuple_key
from .models import VerificationRequest, VerificationResult
from .mock_service import MockTRQPService
from .snapshot import SnapshotStore
from .gateway import TrustGateway


class RevocationDelta:
    """Model for revocation delta updates."""

    def __init__(self, revoked_entities: list[str], policy_epoch: Optional[str] = None) -> None:
        self.revoked_entities = set(revoked_entities)
        self.policy_epoch = policy_epoch
        self.timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def apply(self, entity_id: str) -> tuple[bool, Optional[str]]:
        if entity_id in self.revoked_entities:
            return True, f"revoked_in_epoch_{self.policy_epoch or 'unknown'}"
        return False, None


class Verifier:
    def __init__(
        self,
        *,
        service: MockTRQPService | None = None,
        snapshot: SnapshotStore | None = None,
        cache: TTLCache | None = None,
        gateway: TrustGateway | None = None,
    ) -> None:
        self.service = service
        self.snapshot = snapshot
        self.cache = cache or TTLCache()
        self.revocation_delta: Optional[RevocationDelta] = None
        self.gateway = gateway

    def apply_revocation_delta(self, revoked_entities: list[str], policy_epoch: Optional[str] = None) -> None:
        self.revocation_delta = RevocationDelta(revoked_entities, policy_epoch)

    def verify(self, request: VerificationRequest, profile: str = "standard") -> VerificationResult:
        if not request.integrity_ok:
            return VerificationResult(
                asset_integrity="failed",
                assertion_binding="unknown",
                issuer_recognition="unknown",
                actor_authorization="unknown",
                process_integrity="unknown",
                policy_freshness="n/a",
                verification_mode="local_only",
                trust_outcome="rejected",
                explanations=["Asset integrity verification failed"],
            )

        if self.revocation_delta is not None:
            is_revoked, reason = self.revocation_delta.apply(request.entity_id)
            if is_revoked:
                return VerificationResult(
                    asset_integrity="verified",
                    assertion_binding="verified",
                    issuer_recognition="unknown",
                    actor_authorization="not_authorized",
                    process_integrity="not_evaluated",
                    policy_freshness="revoked",
                    verification_mode="revocation_check",
                    trust_outcome="rejected",
                    explanations=[f"Entity revoked: {reason}"],
                )

        auth_key = tuple_key(request.entity_id, request.authority_id, request.action, request.resource, request.context)
        rec_context = {}
        if "credential_type" in request.context:
            rec_context["credential_type"] = request.context["credential_type"]
        rec_key = tuple_key(request.authority_id, request.issuer_id or "", "recognition", "issuer", rec_context)

        if profile == "edge":
            return self._verify_edge(request, rec_context)
        if profile == "high_assurance":
            return self._verify_online(request, auth_key, rec_key, rec_context, force_live=True)
        return self._verify_online(request, auth_key, rec_key, rec_context, force_live=False)

    def _verify_edge(self, request: VerificationRequest, rec_context: dict) -> VerificationResult:
        if self.snapshot is None:
            return VerificationResult(
                asset_integrity="verified",
                assertion_binding="verified",
                issuer_recognition="unknown",
                actor_authorization="unknown",
                process_integrity="unknown",
                policy_freshness="missing_snapshot",
                verification_mode="offline_snapshot",
                trust_outcome="deferred",
                explanations=["No snapshot available for edge verification"],
            )

        if not self.snapshot.is_usable():
            return VerificationResult(
                asset_integrity="verified",
                assertion_binding="verified",
                issuer_recognition="unknown",
                actor_authorization="unknown",
                process_integrity="unknown",
                policy_freshness=self.snapshot.status(),
                verification_mode="offline_snapshot",
                trust_outcome="rejected",
                explanations=[f"Snapshot validation failed: {err}" for err in self.snapshot.validation_errors],
            )

        auth = self.snapshot.find_authorization(
            request.entity_id, request.authority_id, request.action, request.resource, request.context
        )
        rec = None
        if request.issuer_id:
            rec = self.snapshot.find_recognition(request.authority_id, request.issuer_id, rec_context)
        return self._synthesize_result(auth=auth, rec=rec, freshness=self.snapshot.status(), mode="offline_snapshot", request=request)

    def _verify_online(
        self,
        request: VerificationRequest,
        auth_key: str,
        rec_key: str,
        rec_context: dict,
        force_live: bool,
    ) -> VerificationResult:
        auth = None if force_live else self.cache.get(auth_key)
        rec = None if force_live else self.cache.get(rec_key)
        explanations = []
        gateway_mediation: dict[str, Any] = {}

        if auth is None:
            if self.service is None and self.gateway is None:
                return VerificationResult(
                    asset_integrity="verified",
                    assertion_binding="verified",
                    issuer_recognition="unknown",
                    actor_authorization="unknown",
                    process_integrity="unknown",
                    policy_freshness="service_unavailable",
                    verification_mode="cached_online",
                    trust_outcome="deferred",
                    explanations=["No service or gateway available for live authorization lookup"],
                )
            if self.gateway is not None:
                auth, gateway_mediation = self.gateway.authorization(
                    request.entity_id, request.authority_id, request.action, request.resource, request.context
                )
                explanations.append("Trust gateway mediated authorization lookup")
            else:
                auth = asdict(
                    self.service.authorization(
                        request.entity_id, request.authority_id, request.action, request.resource, request.context
                    )
                )
                explanations.append("Live authorization lookup executed")
            self.cache.set(auth_key, auth, ttl_class="medium")
        else:
            explanations.append("Authorization cache hit")

        if request.issuer_id:
            if rec is None:
                if self.gateway is not None:
                    rec, rec_mediation = self.gateway.recognition(request.authority_id, request.issuer_id, rec_context)
                    gateway_mediation = {**gateway_mediation, 'recognition': rec_mediation}
                    self.cache.set(rec_key, rec, ttl_class="medium")
                    explanations.append("Trust gateway mediated recognition lookup")
                elif self.service is not None:
                    rec = asdict(self.service.recognition(request.authority_id, request.issuer_id, rec_context))
                    self.cache.set(rec_key, rec, ttl_class="medium")
                    explanations.append("Live recognition lookup executed")
            else:
                explanations.append("Recognition cache hit")

        result = self._synthesize_result(
            auth=auth,
            rec=rec,
            freshness="current",
            mode="gateway_mediated" if self.gateway is not None else ("online_full" if force_live else "cached_online"),
            request=request,
            gateway_mediation=gateway_mediation,
        )
        result.explanations.extend(explanations)
        return result

    def _appraise_process(self, request: VerificationRequest, policy_requirements: dict[str, Any]) -> tuple[str, dict[str, Any], list[str], bool]:
        evidence = request.process_evidence
        requires_process = bool(policy_requirements.get("requires_process_proof"))
        min_confidence = float(policy_requirements.get("min_process_integrity", 0.0) or 0.0)
        allowed_types = policy_requirements.get("allowed_process_types", []) or []

        if not evidence:
            if requires_process:
                return (
                    "missing_required_proof",
                    {"status": "missing", "required": True, "minimum_confidence": min_confidence},
                    ["Authorization policy requires process proof but no process evidence was supplied"],
                    False,
                )
            return ("not_evaluated", {"status": "not_evaluated"}, [], True)

        confidence = float(evidence.get("confidence", 0.0) or 0.0)
        verified = bool(evidence.get("verified", False))
        process_type = evidence.get("process_type", "unspecified")
        summary = {
            "status": "verified" if verified else "failed",
            "process_type": process_type,
            "confidence": confidence,
            "minimum_confidence": min_confidence,
            "evidence_ref": evidence.get("evidence_ref"),
            "evidence_format": evidence.get("evidence_format"),
            "appraisal": evidence.get("appraisal"),
            "reference": evidence.get("reference"),
        }
        explanations = []
        passes = True

        if not verified:
            passes = False
            explanations.append("Process evidence was present but did not verify")

        if allowed_types and process_type not in allowed_types:
            passes = False
            explanations.append(f"Process type {process_type} is not allowed by policy")

        if confidence < min_confidence:
            passes = False
            explanations.append(
                f"Process confidence {confidence:.2f} is below policy minimum {min_confidence:.2f}"
            )

        if not passes:
            if not verified:
                return ("failed", summary, explanations, False)
            return ("insufficient", summary, explanations, False)

        if confidence >= 0.85:
            return ("verified_high", summary, explanations, True)
        return ("verified", summary, explanations, True)

    def _synthesize_result(self, *, auth: dict | None, rec: dict | None, freshness: str, mode: str, request: VerificationRequest, gateway_mediation: dict[str, Any] | None = None) -> VerificationResult:
        actor_authorization = "authorized" if auth and auth.get("authorized") else "not_authorized"
        issuer_recognition = "recognized" if rec and rec.get("recognized") else "unknown"
        policy_requirements = auth.get("policy_requirements", {}) if auth else {}
        process_integrity, process_appraisal, process_explanations, process_ok = self._appraise_process(request, policy_requirements)
        policy_evidence = {
            'authorization_evidence': auth.get('evidence', []) if auth else [],
            'recognition_evidence': rec.get('evidence', []) if rec else [],
            'policy_epoch': auth.get('policy_epoch') if auth else None,
            'policy_requirements': policy_requirements,
        }

        if auth is None:
            return VerificationResult(
                asset_integrity="verified",
                assertion_binding="verified",
                issuer_recognition=issuer_recognition,
                actor_authorization="unknown",
                process_integrity=process_integrity,
                policy_freshness=freshness,
                verification_mode=mode,
                trust_outcome="deferred",
                process_appraisal=process_appraisal,
                policy_evidence=policy_evidence,
                gateway_mediation=gateway_mediation or {},
                explanations=process_explanations,
            )

        trust_outcome = "trusted" if actor_authorization == "authorized" else "rejected"
        explanations = list(process_explanations)
        if actor_authorization == "authorized" and not process_ok:
            trust_outcome = "rejected"
            explanations.insert(0, "Authorization passed but process policy requirements were not met")
        if mode == "offline_snapshot" and actor_authorization == "authorized" and process_ok:
            trust_outcome = "trusted_cached"

        return VerificationResult(
            asset_integrity="verified",
            assertion_binding="verified",
            issuer_recognition=issuer_recognition,
            actor_authorization=actor_authorization,
            process_integrity=process_integrity,
            policy_freshness=freshness,
            verification_mode=mode,
            trust_outcome=trust_outcome,
            process_appraisal=process_appraisal,
            policy_evidence=policy_evidence,
            gateway_mediation=gateway_mediation or {},
            explanations=explanations,
        )
