from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey

from .jsoncanon import sha256_hex


class FeedDescriptorError(Exception):
    """Raised when a feed descriptor cannot be validated."""


FRESHNESS_REASON_CODES = {
    "fresh",
    "stale_but_warned",
    "stale_rejected",
    "missing_feed_descriptor",
    "descriptor_signature_invalid",
    "descriptor_digest_mismatch",
    "authority_not_recognized",
    "route_unattested",
    "revocation_channel_degraded",
}


def _parse_utc(ts: str | None) -> datetime | None:
    if not ts:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(timezone.utc)


def canonical_descriptor_payload(descriptor: dict[str, Any]) -> bytes:
    content = dict(descriptor)
    content.pop("descriptor_signature", None)
    return json.dumps(content, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign_feed_descriptor(descriptor: dict[str, Any], private_key: Ed25519PrivateKey, *, key_id: str) -> dict[str, Any]:
    signed = dict(descriptor)
    signed.pop("descriptor_signature", None)
    signature = private_key.sign(canonical_descriptor_payload(signed))
    signed["descriptor_signature"] = {
        "algorithm": "Ed25519",
        "key_id": key_id,
        "value": base64.b64encode(signature).decode("ascii"),
    }
    return signed


def sign_feed_descriptor_from_path(descriptor: dict[str, Any], private_key_path: str | Path, *, key_id: str) -> dict[str, Any]:
    private_key = serialization.load_pem_private_key(Path(private_key_path).read_bytes(), password=None)
    if not isinstance(private_key, Ed25519PrivateKey):
        raise FeedDescriptorError("feed descriptor signing key must be an Ed25519 private key")
    return sign_feed_descriptor(descriptor, private_key, key_id=key_id)


def load_trust_anchor(trust_anchors: dict[str, Any], key_id: str) -> dict[str, Any] | None:
    return next((item for item in trust_anchors.get("keys", []) if item.get("key_id") == key_id), None)


def validate_feed_descriptor_signature(descriptor: dict[str, Any], trust_anchors: dict[str, Any]) -> tuple[bool, str | None]:
    signature = descriptor.get("descriptor_signature")
    if not signature:
        return False, "missing descriptor signature"
    if signature.get("algorithm") != "Ed25519" or not signature.get("key_id") or not signature.get("value"):
        return False, "invalid descriptor signature metadata"
    anchor = load_trust_anchor(trust_anchors, signature["key_id"])
    if anchor is None:
        return False, "descriptor signer is not recognized by configured trust anchors"
    try:
        public_key = serialization.load_pem_public_key(anchor["public_key_pem"].encode("utf-8"))
        if not isinstance(public_key, Ed25519PublicKey):
            raise TypeError("not an Ed25519 public key")
        public_key.verify(base64.b64decode(signature["value"]), canonical_descriptor_payload(descriptor))
    except Exception:
        return False, "descriptor signature verification failed"
    return True, None


@dataclass
class FeedValidationReport:
    descriptor_id: str | None
    feed_type: str | None
    authority_id: str | None
    route_attested: bool
    integrity_ok: bool
    authority_ok: bool
    signature_ok: bool
    freshness_ok: bool
    reason_code: str
    violations: list[str] = field(default_factory=list)
    digest_sha256: str | None = None
    declared_digest_sha256: str | None = None
    issued_at: str | None = None
    valid_until: str | None = None
    max_age_seconds: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "descriptor_id": self.descriptor_id,
            "feed_type": self.feed_type,
            "authority_id": self.authority_id,
            "route_attested": self.route_attested,
            "integrity_ok": self.integrity_ok,
            "authority_ok": self.authority_ok,
            "signature_ok": self.signature_ok,
            "freshness_ok": self.freshness_ok,
            "reason_code": self.reason_code,
            "violations": list(self.violations),
            "digest_sha256": self.digest_sha256,
            "declared_digest_sha256": self.declared_digest_sha256,
            "issued_at": self.issued_at,
            "valid_until": self.valid_until,
            "max_age_seconds": self.max_age_seconds,
        }


def validate_feed_descriptor(
    descriptor: dict[str, Any] | None,
    feed_body: str | bytes | dict[str, Any] | list[Any] | None,
    *,
    trust_anchors: dict[str, Any] | None,
    expected_authorities: set[str] | None = None,
    route_required: bool = False,
    now: datetime | None = None,
) -> FeedValidationReport:
    now = now or datetime.now(timezone.utc)
    if descriptor is None:
        return FeedValidationReport(None, None, None, False, False, False, False, False, "missing_feed_descriptor", ["feed descriptor is missing"])

    violations: list[str] = []
    if isinstance(feed_body, bytes):
        body_bytes = feed_body
    elif isinstance(feed_body, str):
        body_bytes = feed_body.encode("utf-8")
    elif feed_body is None:
        body_bytes = b""
    else:
        body_bytes = json.dumps(feed_body, sort_keys=True, separators=(",", ":")).encode("utf-8")

    actual_digest = hashlib.sha256(body_bytes).hexdigest()
    declared_digest = descriptor.get("feed", {}).get("digest_sha256")
    integrity_ok = bool(declared_digest and actual_digest == declared_digest)
    if not integrity_ok:
        violations.append("feed descriptor digest does not match feed body")

    signature_ok = False
    if trust_anchors is None:
        violations.append("trust anchors unavailable for feed descriptor validation")
    else:
        signature_ok, signature_error = validate_feed_descriptor_signature(descriptor, trust_anchors)
        if not signature_ok and signature_error:
            violations.append(signature_error)

    authority_id = descriptor.get("authority", {}).get("authority_id")
    authority_ok = bool(authority_id) and (not expected_authorities or authority_id in expected_authorities)
    if not authority_ok:
        violations.append(f"feed authority {authority_id!r} is not recognized for this verification scope")

    route = descriptor.get("route", {})
    route_attested = bool(route.get("attested", False))
    if route_required and not route_attested:
        violations.append("feed route is not attested")

    valid_until = _parse_utc(descriptor.get("valid_until"))
    freshness_ok = True
    if valid_until is not None and now > valid_until:
        freshness_ok = False
        violations.append("feed descriptor validity window has expired")

    if not signature_ok:
        reason = "descriptor_signature_invalid"
    elif not integrity_ok:
        reason = "descriptor_digest_mismatch"
    elif not authority_ok:
        reason = "authority_not_recognized"
    elif route_required and not route_attested:
        reason = "route_unattested"
    elif not freshness_ok:
        reason = "stale_rejected"
    else:
        reason = "fresh"

    return FeedValidationReport(
        descriptor_id=descriptor.get("descriptor_id"),
        feed_type=descriptor.get("feed", {}).get("feed_type"),
        authority_id=authority_id,
        route_attested=route_attested,
        integrity_ok=integrity_ok,
        authority_ok=authority_ok,
        signature_ok=signature_ok,
        freshness_ok=freshness_ok,
        reason_code=reason,
        violations=violations,
        digest_sha256=actual_digest,
        declared_digest_sha256=declared_digest,
        issued_at=descriptor.get("issued_at"),
        valid_until=descriptor.get("valid_until"),
        max_age_seconds=descriptor.get("freshness", {}).get("max_age_seconds"),
    )


def load_feed_descriptor(path: str | Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))
