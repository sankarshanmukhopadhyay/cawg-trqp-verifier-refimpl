#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"docs"/"sections"/"walkthroughs-index.md"
required={"schema_version","walkthrough_id","title","authority_domain","action","decision_boundary","cases","evidence_outputs","limitations"}
required_cases={"authorized","scope-mismatch","revoked","stale","conflict","corrected"}
errors=[]; checked=0
index_text=INDEX.read_text(encoding="utf-8")
for path in sorted((ROOT/"examples").glob("*/scenario.json")):
    checked+=1
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}"); continue
    missing=required-set(data)
    if missing: errors.append(f"{path.relative_to(ROOT)}: missing fields {sorted(missing)}")
    ids={c.get("id") for c in data.get("cases",[]) if isinstance(c,dict)}
    if ids != required_cases: errors.append(f"{path.relative_to(ROOT)}: case ids must be {sorted(required_cases)}")
    for c in data.get("cases",[]):
        for key in ("id","condition","expected_outcome","reason_code"):
            if not c.get(key): errors.append(f"{path.relative_to(ROOT)}: case missing {key}")
    slug=data.get("walkthrough_id","")
    doc=ROOT/"docs"/"workflows"/(slug+".md")
    if not doc.is_file(): errors.append(f"{path.relative_to(ROOT)}: missing walkthrough document {doc.relative_to(ROOT)}")
    elif f"../workflows/{slug}.md" not in index_text:
        errors.append(f"{path.relative_to(ROOT)}: walkthrough is not discoverable from docs/sections/walkthroughs-index.md")
if checked < 1: errors.append("no machine-readable walkthrough scenario manifests found")
if errors:
    print("walkthrough examples: FAIL")
    for e in errors: print(f"- {e}")
    sys.exit(1)
print(f"walkthrough examples: {checked} discovered manifests OK")
