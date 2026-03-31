from __future__ import annotations

import argparse
import json
from pathlib import Path

from cawg_trqp_refimpl.validation import DEFAULT_AUDIT_BUNDLE_SCHEMA, load_json, validate_audit_bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a CAWG-TRQP audit bundle")
    parser.add_argument("bundle_json", help="Path to audit bundle JSON")
    parser.add_argument("--schema", default=str(DEFAULT_AUDIT_BUNDLE_SCHEMA), help="Path to audit bundle schema")
    args = parser.parse_args()

    bundle = load_json(args.bundle_json)
    schema = load_json(args.schema)
    errors = validate_audit_bundle(bundle, schema)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        raise SystemExit(1)
    print(json.dumps({"valid": True, "bundle_id": bundle.get("bundle_id")}, indent=2))


if __name__ == "__main__":
    main()
