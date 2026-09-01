#!/usr/bin/env python3
"""Validate the machine-readable adversarial falsification contract."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conformance" / "adversarial-vectors.json"
REQUIRED_CLASSES = {
    "delegated_authority_misuse",
    "gateway_route_substitution",
    "revoked_issuer_recognition",
    "partial_provenance_stripping",
    "replay_root_confusion",
}
REQUIRED_FIELDS = {
    "id", "class", "proposition", "mutation", "expected_trust_outcome",
    "expected_reason_code", "assurance_level", "risk_mapping",
}


def validate() -> list[str]:
    errors: list[str] = []
    data = json.loads(PATH.read_text())
    vectors = data.get("vectors", [])
    classes = {vector.get("class") for vector in vectors}
    missing_classes = REQUIRED_CLASSES - classes
    if missing_classes:
        errors.append(f"missing adversarial classes: {sorted(missing_classes)}")

    seen: set[str] = set()
    for vector in vectors:
        missing = REQUIRED_FIELDS - set(vector)
        if missing:
            errors.append(f"{vector.get('id', '<unknown>')}: missing fields {sorted(missing)}")
        vector_id = vector.get("id")
        if vector_id in seen:
            errors.append(f"duplicate vector id: {vector_id}")
        seen.add(vector_id)
        if vector.get("expected_trust_outcome") not in {"rejected", "deferred"}:
            errors.append(f"{vector_id}: adversarial vector must fail safe")
        if not vector.get("expected_reason_code"):
            errors.append(f"{vector_id}: expected reason code is required")
        if not vector.get("risk_mapping"):
            errors.append(f"{vector_id}: risk mapping is required")
        if vector.get("assurance_level") not in {"AL2", "AL3", "AL4"}:
            errors.append(f"{vector_id}: unsupported assurance level")
    return errors


if __name__ == "__main__":
    failures = validate()
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"validated {len(json.loads(PATH.read_text())['vectors'])} adversarial vectors")
