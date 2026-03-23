from __future__ import annotations

from pathlib import Path

from .manifest_parser import CAWGManifestParser
from .models import VerificationRequest


def load_manifest_fixture(path: str | Path, authority_id: str) -> VerificationRequest:
    signal = CAWGManifestParser.parse_file(path)
    raw = signal.raw_manifest
    asset_id = raw.get("asset_id") or raw.get("asset", {}).get("id") or raw.get("manifest_store", {}).get("asset_id") or "asset-unknown"
    integrity_ok = signal.integrity_status != "failed" and raw.get("integrity_ok", True)

    if not signal.action or not signal.resource:
        raise ValueError("Manifest fixture did not produce action/resource signals")

    return VerificationRequest(
        asset_id=asset_id,
        integrity_ok=integrity_ok,
        entity_id=signal.actor_id,
        authority_id=authority_id,
        issuer_id=signal.issuer_id,
        action=signal.action,
        resource=signal.resource,
        context=dict(signal.context),
        process_evidence=dict(signal.process_evidence) if signal.process_evidence else None,
    )
