#!/usr/bin/env python3
"""Validate machine-readable executable adoption journeys against repository artifacts."""
from pathlib import Path
import json
import shlex
import sys

ROOT = Path(__file__).resolve().parents[1]
JOURNEY_DIR = ROOT / "examples" / "adoption-journeys"
OPENAPI = ROOT / "api" / "openapi.json"

errors = []
checked = 0

try:
    openapi = json.loads(OPENAPI.read_text(encoding="utf-8"))
except Exception as exc:
    print(f"adoption journeys: FAIL\n- cannot load {OPENAPI.relative_to(ROOT)}: {exc}")
    sys.exit(1)

paths = openapi.get("paths", {})
required_top = {
    "schema_version",
    "journey_id",
    "title",
    "documentation",
    "purpose",
    "steps",
    "required_outcome_classes",
    "acceptance_probes",
}
required_outcomes = {"allow", "deny", "indeterminate", "review"}

for path in sorted(JOURNEY_DIR.glob("*.json")):
    checked += 1
    rel = path.relative_to(ROOT)
    try:
        journey = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{rel}: invalid JSON: {exc}")
        continue

    missing = required_top - set(journey)
    if missing:
        errors.append(f"{rel}: missing fields {sorted(missing)}")

    doc = ROOT / journey.get("documentation", "")
    if not doc.is_file():
        errors.append(f"{rel}: documentation path does not exist: {journey.get('documentation')!r}")

    outcomes = set(journey.get("required_outcome_classes", []))
    if outcomes != required_outcomes:
        errors.append(f"{rel}: required_outcome_classes must be {sorted(required_outcomes)}")

    steps = journey.get("steps", [])
    if not isinstance(steps, list) or not steps:
        errors.append(f"{rel}: steps must be a non-empty list")
        continue

    seen_ids = set()
    for step in steps:
        if not isinstance(step, dict):
            errors.append(f"{rel}: every step must be an object")
            continue
        sid = step.get("id")
        if not sid:
            errors.append(f"{rel}: step missing id")
        elif sid in seen_ids:
            errors.append(f"{rel}: duplicate step id {sid!r}")
        else:
            seen_ids.add(sid)

        evidence = step.get("evidence")
        if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x for x in evidence):
            errors.append(f"{rel}: step {sid!r} must declare non-empty evidence")

        endpoint = step.get("endpoint")
        if endpoint:
            try:
                method, route = endpoint.split(" ", 1)
            except ValueError:
                errors.append(f"{rel}: step {sid!r} endpoint must be 'METHOD /path'")
            else:
                operation = paths.get(route, {}).get(method.lower())
                if operation is None:
                    errors.append(f"{rel}: step {sid!r} endpoint not present in OpenAPI: {endpoint}")

        input_path = step.get("input")
        if input_path and not (ROOT / input_path).is_file():
            errors.append(f"{rel}: step {sid!r} input does not exist: {input_path}")

        step_doc = step.get("documentation")
        if step_doc and not (ROOT / step_doc).is_file():
            errors.append(f"{rel}: step {sid!r} documentation does not exist: {step_doc}")

        command = step.get("command")
        if command:
            try:
                tokens = shlex.split(command)
            except ValueError as exc:
                errors.append(f"{rel}: step {sid!r} command cannot be parsed: {exc}")
                continue
            for token in tokens:
                if token.startswith("scripts/") or token.startswith("examples/") or token.startswith("data/"):
                    candidate = ROOT / token
                    if not candidate.exists():
                        errors.append(f"{rel}: step {sid!r} command references missing path: {token}")

    probes = journey.get("acceptance_probes", [])
    if not isinstance(probes, list) or len(probes) < 5 or len(set(probes)) != len(probes):
        errors.append(f"{rel}: acceptance_probes must contain at least five unique probes")

if checked < 1:
    errors.append("no executable adoption journey manifests found")

if errors:
    print("adoption journeys: FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"adoption journeys: {checked} journey manifest(s) resolve to live docs, endpoints, commands, and evidence")
