from __future__ import annotations
import hashlib
import json


def normalize_context(context: dict) -> dict:
    return dict(sorted(context.items(), key=lambda kv: kv[0]))


def context_hash(context: dict) -> str:
    normalized = normalize_context(context)
    payload = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def tuple_key(entity_id: str, authority_id: str, action: str, resource: str, context: dict) -> str:
    return "|".join([entity_id, authority_id, action, resource, context_hash(context)])
