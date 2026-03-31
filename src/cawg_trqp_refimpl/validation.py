from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .jsoncanon import sha256_hex


class BundleValidationError(Exception):
    """Raised when an audit bundle fails structural or deterministic validation."""


DEFAULT_AUDIT_BUNDLE_SCHEMA = Path(__file__).resolve().parents[2] / "schemas" / "audit-bundle.schema.json"


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_audit_bundle(bundle: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(bundle), key=lambda err: list(err.path))
    messages = [f"schema: {'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}" for err in errors]

    expected_digest = bundle.get("bundle_digest_sha256")
    if expected_digest:
        content = dict(bundle)
        content.pop("bundle_digest_sha256", None)
        actual_digest = sha256_hex(content)
        if actual_digest != expected_digest:
            messages.append("determinism: bundle_digest_sha256 does not match canonical bundle content")

    bundle_id = bundle.get("bundle_id", "")
    if bundle_id and not bundle_id.startswith("urn:trqp:audit-bundle:sha256:"):
        messages.append("determinism: bundle_id must use urn:trqp:audit-bundle:sha256:<digest> format")

    return messages
