from __future__ import annotations

import hmac
import hashlib
from typing import Any


def keyed_digest(value: str | None, key: bytes = b"cawg-trqp-reference-only") -> str | None:
    if value is None:
        return None
    return "hmac-sha256:" + hmac.new(key, value.encode("utf-8"), hashlib.sha256).hexdigest()


def redact_request(request: dict[str, Any], *, include_raw: bool, include_process_evidence: bool, pseudonymize: bool) -> dict[str, Any]:
    if include_raw:
        output = dict(request)
        if not include_process_evidence:
            output.pop("process_evidence", None)
        return output
    output = {
        "asset_id_digest": keyed_digest(str(request.get("asset_id"))) if request.get("asset_id") is not None else None,
        "entity_id_digest": keyed_digest(str(request.get("entity_id"))) if request.get("entity_id") is not None else None,
        "authority_id": request.get("authority_id"),
        "issuer_id_digest": keyed_digest(str(request.get("issuer_id"))) if request.get("issuer_id") is not None else None,
        "action": request.get("action"),
        "resource_digest": keyed_digest(str(request.get("resource"))) if request.get("resource") is not None else None,
        "context_digest": keyed_digest(repr(sorted((request.get("context") or {}).items()))),
        "has_process_evidence": request.get("process_evidence") is not None,
    }
    if not pseudonymize:
        output.update({k: request.get(k) for k in ("asset_id", "entity_id", "issuer_id", "resource")})
    return output
