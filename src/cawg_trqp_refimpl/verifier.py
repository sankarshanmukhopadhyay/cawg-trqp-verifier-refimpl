"""CAWG–TRQP verifier orchestrating trust decisions across online, cached, and offline modes."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from typing import Optional

from .cache import TTLCache
from .context import tuple_key
from .models import VerificationRequest, VerificationResult
from .mock_service import MockTRQPService
from .snapshot import SnapshotStore


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
    ) -> None:
        self.service = service
        self.snapshot = snapshot
        self.cache = cache or TTLCache()
        self.revocation_delta: Optional[RevocationDelta] = None

    def apply_revocation_delta(self, revoked_entities: list[str], policy_epoch: Optional[str] = None) -> None:
        self.revocation_delta = RevocationDelta(revoked_entities, policy_epoch)

    def verify(self, request: VerificationRequest, profile: str = "standard") -> VerificationResult:
        if not request.integrity_ok:
            return VerificationResult(
                asset_integrity="failed",
                assertion_binding="unknown",
                issuer_recognition="unknown",
                actor_authorization="unknown",
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
        return self._synthesize_result(auth=auth, rec=rec, freshness=self.snapshot.status(), mode="offline_snapshot")

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

        if auth is None:
            if self.service is None:
                return VerificationResult(
                    asset_integrity="verified",
                    assertion_binding="verified",
                    issuer_recognition="unknown",
                    actor_authorization="unknown",
                    policy_freshness="service_unavailable",
                    verification_mode="cached_online",
                    trust_outcome="deferred",
                    explanations=["No service available for live authorization lookup"],
                )
            auth = asdict(
                self.service.authorization(
                    request.entity_id, request.authority_id, request.action, request.resource, request.context
                )
            )
            self.cache.set(auth_key, auth, ttl_class="medium")
            explanations.append("Live authorization lookup executed")
        else:
            explanations.append("Authorization cache hit")

        if request.issuer_id:
            if rec is None:
                if self.service is not None:
                    rec = asdict(self.service.recognition(request.authority_id, request.issuer_id, rec_context))
                    self.cache.set(rec_key, rec, ttl_class="medium")
                    explanations.append("Live recognition lookup executed")
            else:
                explanations.append("Recognition cache hit")

        result = self._synthesize_result(
            auth=auth,
            rec=rec,
            freshness="current",
            mode="online_full" if force_live else "cached_online",
        )
        result.explanations.extend(explanations)
        return result

    def _synthesize_result(self, *, auth: dict | None, rec: dict | None, freshness: str, mode: str) -> VerificationResult:
        actor_authorization = "authorized" if auth and auth.get("authorized") else "not_authorized"
        issuer_recognition = "recognized" if rec and rec.get("recognized") else "unknown"

        if auth is None:
            return VerificationResult(
                asset_integrity="verified",
                assertion_binding="verified",
                issuer_recognition=issuer_recognition,
                actor_authorization="unknown",
                policy_freshness=freshness,
                verification_mode=mode,
                trust_outcome="deferred",
                explanations=[],
            )

        trust_outcome = "trusted" if actor_authorization == "authorized" else "rejected"
        if mode == "offline_snapshot" and actor_authorization == "authorized":
            trust_outcome = "trusted_cached"

        return VerificationResult(
            asset_integrity="verified",
            assertion_binding="verified",
            issuer_recognition=issuer_recognition,
            actor_authorization=actor_authorization,
            policy_freshness=freshness,
            verification_mode=mode,
            trust_outcome=trust_outcome,
            explanations=[],
        )
