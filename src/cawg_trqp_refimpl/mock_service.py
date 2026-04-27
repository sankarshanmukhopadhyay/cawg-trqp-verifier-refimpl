from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from .models import AuthorizationResponse, RecognitionResponse
from .transport import FeedTransportMetadata
from .feed_descriptor import load_feed_descriptor, validate_feed_descriptor


def _parse_utc(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)


class MockTRQPService:
    def __init__(
        self,
        policy_path: str | Path,
        revocation_path: str | Path | None = None,
        *,
        transport_mode: str = "http",
        transport_integrity: str = "tls",
        transport_available: bool = True,
        policy_descriptor_path: str | Path | None = None,
        revocation_descriptor_path: str | Path | None = None,
        trust_anchors_path: str | Path | None = "data/trust_anchors.json",
    ) -> None:
        self.policy_path = Path(policy_path)
        self.policy_body_text = self.policy_path.read_text(encoding="utf-8")
        self.data = json.loads(self.policy_body_text)
        self.revocations = {"revoked_entities": [], "channel": "delta", "issued_at": "2026-12-31T00:00:00Z"}
        self.revocation_body_text = json.dumps(self.revocations, sort_keys=True, separators=(",", ":"))
        if revocation_path is not None:
            self.revocation_body_text = Path(revocation_path).read_text(encoding="utf-8")
            self.revocations = json.loads(self.revocation_body_text)
        self.transport_metadata = FeedTransportMetadata(
            mode=transport_mode,
            integrity=transport_integrity,
            available=transport_available,
            channel=self.revocations.get("channel", "full"),
        )
        self.policy_descriptor = load_feed_descriptor(policy_descriptor_path)
        self.revocation_descriptor = load_feed_descriptor(revocation_descriptor_path)
        self.trust_anchors = json.loads(Path(trust_anchors_path).read_text(encoding="utf-8")) if trust_anchors_path else None
        self.feed_validation = self._validate_feed_descriptors()

    def _validate_feed_descriptors(self) -> dict:
        expected = {"did:web:media-registry.example"}
        return {
            "policy": validate_feed_descriptor(self.policy_descriptor, self.policy_body_text, trust_anchors=self.trust_anchors, expected_authorities=expected).to_dict(),
            "revocation": validate_feed_descriptor(self.revocation_descriptor, self.revocation_body_text, trust_anchors=self.trust_anchors, expected_authorities=expected).to_dict(),
        }

    def feed_descriptor_evidence(self) -> dict:
        return self.feed_validation

    def authorization(self, entity_id: str, authority_id: str, action: str, resource: str, context: dict) -> AuthorizationResponse:
        if entity_id in self.revocations.get("revoked_entities", []):
            return AuthorizationResponse(authorized=False, reason="entity_revoked", policy_epoch=self.revocations.get("policy_epoch"))

        for item in self.data.get("authorization", []):
            if (
                item.get("entity_id") == entity_id
                and item.get("authority_id") == authority_id
                and item.get("action") == action
                and item.get("resource") == resource
                and all(context.get(k) == v for k, v in item.get("context", {}).items())
            ):
                return AuthorizationResponse(
                    authorized=item.get("authorized", False),
                    expires=item.get("expires"),
                    policy_epoch=item.get("policy_epoch"),
                    evidence=item.get("evidence", []),
                    reason=item.get("reason"),
                    policy_requirements=item.get("policy_requirements", {}),
                )
        return AuthorizationResponse(authorized=False, reason="no_matching_policy")

    def recognition(self, authority_id: str, recognized_authority_id: str, context: dict) -> RecognitionResponse:
        for item in self.data.get("recognition", []):
            if (
                item.get("authority_id") == authority_id
                and item.get("recognized_authority_id") == recognized_authority_id
                and all(context.get(k) == v for k, v in item.get("context", {}).items())
            ):
                return RecognitionResponse(
                    recognized=item.get("recognized", False),
                    expires=item.get("expires"),
                    policy_epoch=item.get("policy_epoch"),
                    evidence=item.get("evidence", []),
                    reason=item.get("reason"),
                )
        return RecognitionResponse(recognized=False, reason="not_recognized")

    def revocation_status(self) -> dict:
        issued_at = self.revocations.get("issued_at")
        return {
            "issued_at": issued_at,
            "policy_epoch": self.revocations.get("policy_epoch"),
            "channel": self.revocations.get("channel", "snapshot"),
            "age_seconds": self.revocation_age_seconds(),
            "feed_descriptor": self.feed_validation.get("revocation", {}),
        }

    def revocation_age_seconds(self) -> int | None:
        issued = _parse_utc(self.revocations.get("issued_at"))
        if issued is None:
            return None
        delta = datetime.now(timezone.utc) - issued
        return max(int(delta.total_seconds()), 0)
