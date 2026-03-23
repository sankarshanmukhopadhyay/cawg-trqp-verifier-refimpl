from __future__ import annotations

import base64
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


class SnapshotValidationError(Exception):
    """Raised when snapshot verification fails."""


class SnapshotStore:
    def __init__(
        self,
        path: str | Path,
        trust_anchors_path: str | Path | None = None,
        *,
        verify_signatures: bool = True,
        require_fresh: bool = True,
        current_time: datetime | None = None,
    ) -> None:
        self.path = Path(path)
        self.data = json.loads(self.path.read_text(encoding="utf-8"))
        self.trust_anchors_path = Path(trust_anchors_path) if trust_anchors_path is not None else None
        self.verify_signatures = verify_signatures
        self.require_fresh = require_fresh
        self.current_time = current_time or datetime.now(timezone.utc)
        self.validation_errors: list[str] = []
        self.signature_verified = False

        if self.verify_signatures:
            self._verify_signature()
        self._enforce_freshness()

    def is_usable(self) -> bool:
        return not self.validation_errors

    def status(self) -> str:
        if self.validation_errors:
            return self.validation_errors[0]
        return "snapshot_verified" if self.signature_verified else "snapshot"

    def _verify_signature(self) -> None:
        signature_block = self.data.get("signature")
        if not isinstance(signature_block, dict):
            self.validation_errors.append("missing_snapshot_signature")
            return

        key_id = signature_block.get("key_id")
        algorithm = signature_block.get("algorithm")
        signature_b64 = signature_block.get("value")
        if algorithm != "Ed25519" or not key_id or not signature_b64:
            self.validation_errors.append("invalid_snapshot_signature_metadata")
            return

        if self.trust_anchors_path is None:
            self.validation_errors.append("missing_trust_anchors")
            return

        anchors = json.loads(self.trust_anchors_path.read_text(encoding="utf-8"))
        anchor = next((item for item in anchors.get("keys", []) if item.get("key_id") == key_id), None)
        if anchor is None:
            self.validation_errors.append("unknown_snapshot_signer")
            return

        try:
            public_key = serialization.load_pem_public_key(anchor["public_key_pem"].encode("utf-8"))
            if not isinstance(public_key, Ed25519PublicKey):
                raise TypeError("not an Ed25519 public key")
            payload = self._canonical_payload(self.data)
            public_key.verify(base64.b64decode(signature_b64), payload)
            self.signature_verified = True
        except Exception:
            self.validation_errors.append("invalid_snapshot_signature")

    def _enforce_freshness(self) -> None:
        expires_at = self.data.get("expires_at")
        if not expires_at:
            self.validation_errors.append("missing_snapshot_expiry")
            return
        try:
            expiry = self._parse_timestamp(expires_at)
        except ValueError:
            self.validation_errors.append("invalid_snapshot_expiry")
            return

        if self.require_fresh and self.current_time > expiry:
            self.validation_errors.append("expired_snapshot")

    def find_authorization(self, entity_id: str, authority_id: str, action: str, resource: str, context: dict) -> dict | None:
        if not self.is_usable():
            return None
        for item in self.data.get("authorization", []):
            if (
                item.get("entity_id") == entity_id
                and item.get("authority_id") == authority_id
                and item.get("action") == action
                and item.get("resource") == resource
                and all(context.get(k) == v for k, v in item.get("context", {}).items())
            ):
                return item
        return None

    def find_recognition(self, authority_id: str, recognized_authority_id: str, context: dict) -> dict | None:
        if not self.is_usable():
            return None
        for item in self.data.get("recognition", []):
            if (
                item.get("authority_id") == authority_id
                and item.get("recognized_authority_id") == recognized_authority_id
                and all(context.get(k) == v for k, v in item.get("context", {}).items())
            ):
                return item
        return None

    @staticmethod
    def _canonical_payload(data: dict[str, Any]) -> bytes:
        content = dict(data)
        content.pop("signature", None)
        return json.dumps(content, sort_keys=True, separators=(",", ":")).encode("utf-8")

    @staticmethod
    def _parse_timestamp(value: str) -> datetime:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value).astimezone(timezone.utc)
