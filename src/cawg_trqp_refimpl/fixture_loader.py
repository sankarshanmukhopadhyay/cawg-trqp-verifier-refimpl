from __future__ import annotations
import json
from pathlib import Path
from .models import VerificationRequest


def load_manifest_fixture(path: str | Path, authority_id: str) -> VerificationRequest:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    issuer = data.get("issuer", {})
    actor = data.get("actor", {})
    assertion = data.get("assertion", {})
    context = dict(data.get("context", {}))
    if issuer.get("credential_type"):
        context["credential_type"] = issuer["credential_type"]

    return VerificationRequest(
        asset_id=data["asset_id"],
        integrity_ok=data["integrity_ok"],
        entity_id=actor["entity_id"],
        authority_id=authority_id,
        issuer_id=issuer.get("issuer_id"),
        action=assertion["action"],
        resource=assertion["resource"],
        context=context,
    )
