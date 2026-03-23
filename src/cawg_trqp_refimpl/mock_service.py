from __future__ import annotations
import json
from pathlib import Path
from .models import AuthorizationResponse, RecognitionResponse


class MockTRQPService:
    def __init__(self, policy_path: str | Path, revocation_path: str | Path | None = None) -> None:
        self.policy_path = Path(policy_path)
        self.data = json.loads(self.policy_path.read_text(encoding="utf-8"))
        self.revocations = {"revoked_entities": []}
        if revocation_path is not None:
            self.revocations = json.loads(Path(revocation_path).read_text(encoding="utf-8"))

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
        return RecognitionResponse(recognized=False, reason="no_matching_policy")
