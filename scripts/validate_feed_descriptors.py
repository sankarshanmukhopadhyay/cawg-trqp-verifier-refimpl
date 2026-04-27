#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cawg_trqp_refimpl.feed_descriptor import validate_feed_descriptor

SCHEMA = json.loads((ROOT / "schemas/feed-descriptor.schema.json").read_text())
TRUST = json.loads((ROOT / "data/trust_anchors.json").read_text())
EXPECTED = {"did:web:media-registry.example"}


def main() -> int:
    failures = []
    for path in sorted((ROOT / "examples/feed_descriptors").glob("*.json")):
        descriptor = json.loads(path.read_text())
        for err in Draft202012Validator(SCHEMA).iter_errors(descriptor):
            failures.append(f"{path.relative_to(ROOT)} schema: {'/'.join(map(str, err.path)) or '<root>'}: {err.message}")
        source = descriptor["feed"]["source"]
        report = validate_feed_descriptor(descriptor, (ROOT / source).read_text(), trust_anchors=TRUST, expected_authorities=EXPECTED)
        if report.reason_code != "fresh":
            failures.append(f"{path.relative_to(ROOT)} validation: {report.reason_code} {report.violations}")
    if failures:
        print("validate_feed_descriptors.py: FAIL")
        for item in failures:
            print(f" - {item}")
        return 1
    print("validate_feed_descriptors.py: all feed descriptors OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
