#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "portfolio" / "integration-contract.json"
PYPROJECT = ROOT / "pyproject.toml"

EXPECTED = {
    "semantic": ("sankarshanmukhopadhyay/trust-systems-meta-model", "0.24.0"),
    "schemas": ("sankarshanmukhopadhyay/trust-infrastructure-schemas", "0.14.1"),
    "tspp": ("sankarshanmukhopadhyay/TRQP-TSPP", "0.15.0"),
    "conformance": ("sankarshanmukhopadhyay/trqp-conformance-suite", "1.7.0"),
    "assurance": ("sankarshanmukhopadhyay/trqp-assurance-hub", "1.10.0"),
}
REQUIRED_INVALIDATION = {
    "semantic-authority-version-incompatible",
    "schema-authority-version-incompatible",
    "normative-source-version-incompatible",
    "required-evidence-missing",
    "release-identity-mismatch",
}


def fail(message: str) -> None:
    raise SystemExit(f"portfolio integration contract FAILED: {message}")


def main() -> None:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        fail("unsupported schema_version")
    if data.get("release_train", {}).get("contract_version") != "1.0":
        fail("unsupported contract_version")

    pyproject = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, flags=re.MULTILINE)
    if not match:
        fail("cannot resolve pyproject version")
    if data.get("repository", {}).get("version") != match.group(1):
        fail("repository version does not match pyproject.toml")

    for key in ("semantic", "schemas"):
        entry = data.get("authorities", {}).get(key, {})
        expected_repo, expected_version = EXPECTED[key]
        if (entry.get("repository"), entry.get("version")) != (expected_repo, expected_version):
            fail(f"{key} authority pin mismatch")

    for key in ("tspp", "conformance", "assurance"):
        entry = data.get("trqp_components", {}).get(key, {})
        expected_repo, expected_version = EXPECTED[key]
        if (entry.get("repository"), entry.get("version")) != (expected_repo, expected_version):
            fail(f"{key} component pin mismatch")

    missing = [path for path in data.get("local_evidence", []) if not (ROOT / path).is_file()]
    if missing:
        fail("missing local evidence: " + ", ".join(missing))

    triggers = set(data.get("invalidation_triggers", []))
    if not REQUIRED_INVALIDATION.issubset(triggers):
        fail("required invalidation triggers are incomplete")
    if data.get("invalidation_effect") != "integration-status-invalid":
        fail("unexpected invalidation effect")

    print("portfolio integration contract PASSED")


if __name__ == "__main__":
    main()
