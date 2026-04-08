from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


class AuditBundleAttestationError(Exception):
    """Raised when audit bundle attestation signing or verification fails."""



def _canonical_payload(bundle: dict[str, Any]) -> bytes:
    content = dict(bundle)
    content.pop("bundle_attestation", None)
    return json.dumps(content, sort_keys=True, separators=(",", ":")).encode("utf-8")



def sign_audit_bundle(bundle: dict[str, Any], private_key: Ed25519PrivateKey, *, key_id: str) -> dict[str, Any]:
    signed_bundle = dict(bundle)
    signed_bundle.pop("bundle_attestation", None)
    payload = _canonical_payload(signed_bundle)
    signature = private_key.sign(payload)
    signed_bundle["bundle_attestation"] = {
        "algorithm": "Ed25519",
        "key_id": key_id,
        "value": base64.b64encode(signature).decode("ascii"),
    }
    return signed_bundle



def sign_audit_bundle_from_path(bundle: dict[str, Any], private_key_path: str | Path, *, key_id: str) -> dict[str, Any]:
    private_key = serialization.load_pem_private_key(Path(private_key_path).read_bytes(), password=None)
    if not isinstance(private_key, Ed25519PrivateKey):
        raise AuditBundleAttestationError("bundle signing key must be an Ed25519 private key")
    return sign_audit_bundle(bundle, private_key, key_id=key_id)



def verify_audit_bundle_attestation(bundle: dict[str, Any], trust_anchors_path: str | Path) -> list[str]:
    attestation = bundle.get("bundle_attestation")
    if not attestation:
        return []

    key_id = attestation.get("key_id")
    algorithm = attestation.get("algorithm")
    signature_b64 = attestation.get("value")
    if algorithm != "Ed25519" or not key_id or not signature_b64:
        return ["attestation: invalid attestation metadata"]

    anchors = json.loads(Path(trust_anchors_path).read_text(encoding="utf-8"))
    anchor = next((item for item in anchors.get("keys", []) if item.get("key_id") == key_id), None)
    if anchor is None:
        return ["attestation: unknown attestation signer"]

    try:
        public_key = serialization.load_pem_public_key(anchor["public_key_pem"].encode("utf-8"))
        if not isinstance(public_key, Ed25519PublicKey):
            raise TypeError("not an Ed25519 public key")
        public_key.verify(base64.b64decode(signature_b64), _canonical_payload(bundle))
    except Exception:
        return ["attestation: invalid attestation signature"]
    return []
