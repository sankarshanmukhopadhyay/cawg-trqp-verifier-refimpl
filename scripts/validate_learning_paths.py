#!/usr/bin/env python3
"""Validate guided-learning manifests and their local documentation targets."""
from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "_data" / "learning_paths.json"
errors: list[str] = []
try:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"ERROR: cannot read {MANIFEST.relative_to(ROOT)}: {exc}")
    raise SystemExit(1)
paths = data.get("paths", [])
seen: set[str] = set()
if not paths:
    errors.append("manifest defines no learning paths")
for path in paths:
    pid = path.get("id")
    if not pid or pid in seen:
        errors.append(f"missing or duplicate path id: {pid!r}")
    seen.add(pid)
    steps = path.get("steps", [])
    if not steps:
        errors.append(f"{pid}: no steps")
    for number, step in enumerate(steps, 1):
        target = step.get("file")
        if not target:
            errors.append(f"{pid} step {number}: missing file")
            continue
        resolved = ROOT / target
        if not resolved.is_file():
            errors.append(f"{pid} step {number}: missing target {target}")
        if not step.get("outcome"):
            errors.append(f"{pid} step {number}: missing outcome")
if errors:
    print("Guided-learning validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
print(f"Validated {len(paths)} learning paths and {sum(len(p['steps']) for p in paths)} steps.")
