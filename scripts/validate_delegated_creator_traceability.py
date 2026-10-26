#!/usr/bin/env python3
"""Validate traceability manifest structure and repository-local evidence paths.

This is a metadata consistency check, not a claim of CAWG profile conformance.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "conformance" / "delegated-creator-taskforce-traceability.json"
EXPECTED = {f"DC-{i:02d}" for i in range(1, 8)}
STATUSES = {"represented", "partial", "missing", "external"}
NEXT = {"upstream-semantics", "await-taskforce", "local-validation", "none"}

def validate():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0"
    assert data["basis"]["authority"].startswith("informative")
    rows = data["requirements"]
    assert isinstance(rows, list) and len(rows) == 7
    ids = [row["id"] for row in rows]
    assert len(ids) == len(set(ids)) and set(ids) == EXPECTED
    for row in rows:
        assert row["status"] in STATUSES, row["id"]
        assert row["next"] in NEXT, row["id"]
        assert isinstance(row["title"], str) and row["title"].strip()
        assert isinstance(row["gap"], str) and row["gap"].strip()
        assert isinstance(row["evidence"], list) and row["evidence"]
        for path in row["evidence"]:
            target = (ROOT / path).resolve()
            assert target.is_relative_to(ROOT), path
            assert target.is_file(), path

if __name__ == "__main__":
    validate()
    print("Delegated Creator traceability: 7 rows, valid evidence paths; semantic conformance NOT asserted")
