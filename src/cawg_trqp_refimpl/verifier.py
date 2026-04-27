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
from .profile import VerificationProfile, load_profile
from .transport import FeedTransportMetadata, evaluate_transport_constraints


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
        self.last_transport_metadata: dict[str, Any] = {}
        self.last_revocation_status: dict[str, Any] = {}
        self.last_feed_descriptor_evidence: dict[str, Any] = {}

    def apply_revocation_delta(self, revoked_entities: list[str], policy_epoch: Optional[str] = None) -> None:
        self.revocation_delta = RevocationDelta(revoked_entities, policy_epoch)

    def verify(self, request: VerificationRequest, profile: str | dict[str, Any] | VerificationProfile = "standard") -> VerificationResult:
        resolved_profile = load_profile(profile)
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
                explanations=[f"Asset integrity verification failed under profile {resolved_profile.id}"],
            )

        if self.revocation_delta is not None:
            is_revoked, reason = self.revocation_delta.apply(request.entity_id)
            if is_revoked:
                self.last_revocation_status = {
                    "status": "revoked",
                    "source": "delta_cache",
                    "policy_epoch": self.revocation_delta.policy_epoch,
                    "freshness_ok": True,
                }
                return VerificationResult(
                    asset_integrity="verified",
                    assertion_binding="verified",
                    issuer_recognition="unknown",
                    actor_authorization="not_authorized",
                    process_integrity="not_evaluated",
                    policy_freshness="revoked",
                    verification_mode="revocation_check",
                    trust_outcome="rejected",
                    explanations=[f"Entity revoked: {reason}", f"Verification profile: {resolved_profile.id}"],
                    policy_evidence={"verification_profile": resolved_profile.to_dict(), "revocation_status": self.last_revocation_status, "feed_descriptors": self.last_feed_descriptor_evidence},
                )

        auth_key = tuple_key(request.entity_id, request.authority_id, request.action, request.resource, request.context)
        rec_context = {}
        if "credential_type" in request.context:
            rec_context["credential_type"] = request.context["credential_type"]
        rec_key = tuple_key(request.authority_id, request.issuer_id or "", "recognition", "issuer", rec_context)

        base_profile = resolved_profile.base_profile
        if base_profile == "edge":
            return self._verify_edge(request, rec_context, resolved_profile)

        force_live = bool(resolved_profile.controls["freshness"]["require_live"])
        return self._verify_online(request, auth_key, rec_key, rec_context, force_live=force_live, profile=resolved_profile)

    def _current_transport_metadata(self) -> FeedTransportMetadata:
        if self.gateway is not None:
            return self.gateway.transport_metadata
        if self.service is not None:
            return self.service.transport_metadata
        return FeedTransportMetadata(mode='local', integrity='none', available=False, channel='none')

    def _current_feed_descriptor_evidence(self) -> dict[str, Any]:
        if self.gateway is not None and self.gateway.service is not None:
            return self.gateway.service.feed_descriptor_evidence()
        if self.service is not None:
            return self.service.feed_descriptor_evidence()
        return {}

    def _current_revocation_status(self, profile: VerificationProfile) -> dict[str, Any]:
        max_age = profile.controls['revocation'].get('max_age_seconds', 0)
        enforcement = profile.controls['revocation'].get('enforcement', 'warn')
        failures: list[str] = []
        if self.service is not None:
            status = {"source": "service", **self.service.revocation_status()}
        else:
            status = {"source": "none", "channel": "none", "age_seconds": None}

        age_seconds = status.get('age_seconds')
        if age_seconds is not None and age_seconds > max_age:
            failures.append(f"revocation data age {age_seconds}s exceeds allowed window {max_age}s")
        if profile.controls['revocation'].get('delta_channel_required') and status.get('channel') not in {'delta', 'live', 'mediated'}:
            failures.append(f"revocation channel {status.get('channel')!r} does not satisfy required delta/live semantics")

        status['freshness_ok'] = not failures
        status['max_age_seconds'] = max_age
        status['enforcement'] = enforcement
        status['violations'] = list(failures)
        return status

    def _evaluate_transport(self, profile: VerificationProfile) -> tuple[bool, list[str]]:
        actual = self._current_transport_metadata()
        failures = evaluate_transport_constraints(profile.controls['transport'], actual)
        self.last_transport_metadata = {
            "required": dict(profile.controls['transport']),
            "actual": actual.to_dict(),
            "violations": list(failures),
            "satisfied": not failures,
        }
        return (not failures, failures)

    def _evaluate_revocation_freshness(self, profile: VerificationProfile) -> tuple[bool, list[str]]:
        status = self._current_revocation_status(profile)
        self.last_revocation_status = status
        failures = list(status.get('violations', []))
        self.last_feed_descriptor_evidence = self._current_feed_descriptor_evidence()
        for name, report in self.last_feed_descriptor_evidence.items():
            reason = report.get("reason_code")
            if reason in {"descriptor_signature_invalid", "descriptor_digest_mismatch", "authority_not_recognized", "route_unattested", "stale_rejected"}:
                failures.append(f"{name} feed descriptor: {reason}")
        return (not failures, failures)

    def _transport_or_revocation_failure_result(self, profile: VerificationProfile, freshness: str, explanation: str) -> VerificationResult:
        fail_closed = profile.controls['failure']['network_failure'] == 'fail_closed' or profile.controls['revocation'].get('enforcement') == 'fail'
        trust_outcome = 'rejected' if fail_closed else 'deferred'
        return VerificationResult(
            asset_integrity='verified',
            assertion_binding='verified',
            issuer_recognition='unknown',
            actor_authorization='unknown',
            process_integrity='unknown',
            policy_freshness=freshness,
            verification_mode='transport_guardrail',
            trust_outcome=trust_outcome,
            policy_evidence={
                'verification_profile': profile.to_dict(),
                'transport': self.last_transport_metadata,
                'revocation_status': self.last_revocation_status,
                'feed_descriptors': self.last_feed_descriptor_evidence,
            },
            explanations=[explanation],
        )

    def _service_unavailable_result(self, profile: VerificationProfile) -> VerificationResult:
        fail_closed = profile.controls["failure"]["network_failure"] == "fail_closed"
        trust_outcome = "rejected" if fail_closed else "deferred"
        explanation = (
            "No service or gateway available for live authorization lookup; profile requires fail-closed handling"
            if fail_closed
            else "No service or gateway available for live authorization lookup"
        )
        return VerificationResult(
            asset_integrity="verified",
            assertion_binding="verified",
            issuer_recognition="unknown",
            actor_authorization="unknown",
            process_integrity="unknown",
            policy_freshness="service_unavailable",
            verification_mode="online_full" if profile.controls["freshness"]["require_live"] else "cached_online",
            trust_outcome=trust_outcome,
            policy_evidence={"verification_profile": profile.to_dict(), "transport": self.last_transport_metadata, "revocation_status": self.last_revocation_status, "feed_descriptors": self.last_feed_descriptor_evidence},
            explanations=[explanation],
        )

    def _verify_edge(self, request: VerificationRequest, rec_context: dict[str, Any], profile: VerificationProfile) -> VerificationResult:
        self.last_transport_metadata = {
            'required': dict(profile.controls['transport']),
            'actual': FeedTransportMetadata(mode='local', integrity='signed', available=self.snapshot is not None, channel='snapshot').to_dict(),
            'violations': [],
            'satisfied': True,
        }
        self.last_revocation_status = {'source':'snapshot','channel':'snapshot','freshness_ok':True,'violations':[], 'max_age_seconds': profile.controls['revocation'].get('max_age_seconds')}
        if self.snapshot is None:
            return VerificationResult(
                asset_integrity="verified",
                assertion_binding="verified",
                issuer_recognition="unknown",
                actor_authorization="unknown",
                process_integrity="unknown",
                policy_freshness="missing_snapshot",
                verification_mode="offline_snapshot",
                trust_outcome="rejected" if profile.controls["authority"]["trust_anchors_required"] else "deferred",
                policy_evidence={"verification_profile": profile.to_dict(), "transport": self.last_transport_metadata, "revocation_status": self.last_revocation_status, "feed_descriptors": self.last_feed_descriptor_evidence},
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
                policy_evidence={"verification_profile": profile.to_dict(), "transport": self.last_transport_metadata, "revocation_status": self.last_revocation_status, "feed_descriptors": self.last_feed_descriptor_evidence},
                explanations=[f"Snapshot validation failed: {err}" for err in self.snapshot.validation_errors],
            )

        auth = self.snapshot.find_authorization(
            request.entity_id, request.authority_id, request.action, request.resource, request.context
        )
        rec = None
        if request.issuer_id:
            rec = self.snapshot.find_recognition(request.authority_id, request.issuer_id, rec_context)
        return self._synthesize_result(
            auth=auth,
            rec=rec,
            freshness=self.snapshot.status(),
            mode="offline_snapshot",
            request=request,
            profile=profile,
        )

    def _verify_online(
        self,
        request: VerificationRequest,
        auth_key: str,
        rec_key: str,
        rec_context: dict[str, Any],
        force_live: bool,
        profile: VerificationProfile,
    ) -> VerificationResult:
        if self.service is None and self.gateway is None:
            self.last_transport_metadata = {
                'required': dict(profile.controls['transport']),
                'actual': FeedTransportMetadata(mode='local', integrity='none', available=False, channel='none').to_dict(),
                'violations': [],
                'satisfied': False,
            }
            self.last_revocation_status = {'source': 'none', 'freshness_ok': False, 'violations': ['no revocation source available']}
            return self._service_unavailable_result(profile)

        transport_ok, transport_failures = self._evaluate_transport(profile)
        revocation_ok, revocation_failures = self._evaluate_revocation_freshness(profile)
        if not transport_ok:
            return self._transport_or_revocation_failure_result(profile, 'transport_violation', '; '.join(transport_failures))
        if not revocation_ok and profile.controls['revocation'].get('enforcement') == 'fail':
            return self._transport_or_revocation_failure_result(profile, 'revocation_stale', '; '.join(revocation_failures))

        auth = None if force_live else self.cache.get(auth_key)
        rec = None if force_live else self.cache.get(rec_key)
        explanations = [f"Verification profile: {profile.id}"]
        gateway_mediation: dict[str, Any] = {}
        if revocation_failures:
            explanations.append('; '.join(revocation_failures))

        if auth is None:
            if self.service is None and self.gateway is None:
                return self._service_unavailable_result(profile)
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
                    gateway_mediation = {**gateway_mediation, "recognition": rec_mediation}
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
            freshness="fresh" if revocation_ok else 'stale_but_warned',
            mode="gateway_mediated" if self.gateway is not None else ("online_full" if force_live else "cached_online"),
            request=request,
            profile=profile,
            gateway_mediation=gateway_mediation,
        )
        result.explanations.extend(explanations)
        return result

    def _appraise_process(
        self,
        request: VerificationRequest,
        policy_requirements: dict[str, Any],
    ) -> tuple[str, dict[str, Any], list[str], bool]:
        evidence = request.process_evidence or {}
        summary = {
            'status': 'not_evaluated',
            'process_type': evidence.get('process_type'),
            'confidence': evidence.get('confidence'),
            'minimum_confidence': policy_requirements.get('min_process_integrity'),
            'evidence_ref': evidence.get('evidence_ref'),
            'evidence_format': evidence.get('evidence_format'),
            'appraisal': evidence.get('appraisal'),
            'reference': evidence.get('reference'),
        }
        explanations: list[str] = []
        requires_process = bool(policy_requirements.get('requires_process_proof'))
        if not requires_process:
            summary['status'] = 'not_required'
            return ('not_required', summary, explanations, True)

        if not evidence:
            summary['status'] = 'missing_required_proof'
            return ('missing_required_proof', summary, ['Policy requires process proof but request did not include process evidence'], False)

        verified = bool(evidence.get('verified'))
        process_type = evidence.get('process_type')
        confidence = float(evidence.get('confidence', 0.0) or 0.0)
        min_confidence = float(policy_requirements.get('min_process_integrity', 0.0) or 0.0)
        allowed_types = policy_requirements.get('allowed_process_types', [])

        summary['status'] = 'verified' if verified else 'failed'
        passes = verified

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
                return ('failed', summary, explanations, False)
            return ('insufficient', summary, explanations, False)

        if confidence >= 0.85:
            return ('verified_high', summary, explanations, True)
        return ('verified', summary, explanations, True)

    def _synthesize_result(
        self,
        *,
        auth: dict | None,
        rec: dict | None,
        freshness: str,
        mode: str,
        request: VerificationRequest,
        profile: VerificationProfile,
        gateway_mediation: dict[str, Any] | None = None,
    ) -> VerificationResult:
        actor_authorization = "authorized" if auth and auth.get("authorized") else "not_authorized"
        issuer_recognition = "recognized" if rec and rec.get("recognized") else "unknown"
        policy_requirements = auth.get("policy_requirements", {}) if auth else {}
        process_integrity, process_appraisal, process_explanations, process_ok = self._appraise_process(request, policy_requirements)
        policy_evidence = {
            "authorization_evidence": auth.get("evidence", []) if auth else [],
            "recognition_evidence": rec.get("evidence", []) if rec else [],
            "policy_epoch": auth.get("policy_epoch") if auth else None,
            "policy_requirements": policy_requirements,
            "verification_profile": profile.to_dict(),
            "transport": self.last_transport_metadata,
            "revocation_status": self.last_revocation_status,
            "feed_descriptors": self.last_feed_descriptor_evidence,
        }

        if auth is None:
            trust_outcome = "rejected" if profile.controls["failure"]["policy_unavailable"] == "fail_closed" else "deferred"
            return VerificationResult(
                asset_integrity="verified",
                assertion_binding="verified",
                issuer_recognition=issuer_recognition,
                actor_authorization="unknown",
                process_integrity=process_integrity,
                policy_freshness=freshness,
                verification_mode=mode,
                trust_outcome=trust_outcome,
                process_appraisal=process_appraisal,
                policy_evidence=policy_evidence,
                gateway_mediation=gateway_mediation or {},
                explanations=process_explanations,
            )

        if actor_authorization == "authorized" and issuer_recognition == "unknown" and not profile.controls["authority"]["allow_untrusted"]:
            actor_authorization = "not_authorized"
            process_ok = False
            process_explanations = [
                "Authorization matched but issuer recognition is required by profile authority controls"
            ] + process_explanations

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
