#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
required={"schema_version","walkthrough_id","title","authority_domain","action","decision_boundary","cases","evidence_outputs","limitations"}
required_cases={"authorized","scope-mismatch","revoked","stale","conflict","corrected"}
errors=[]; checked=0
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
    doc=ROOT/"docs"/"workflows"/(data.get("walkthrough_id","")+".md")
    if not doc.is_file(): errors.append(f"{path.relative_to(ROOT)}: missing walkthrough document {doc.relative_to(ROOT)}")
if checked != 10: errors.append(f"expected 10 v0.18.1 scenario manifests, found {checked}")
if errors:
    print("walkthrough examples: FAIL")
    for e in errors: print(f"- {e}")
    sys.exit(1)
print(f"walkthrough examples: {checked}/10 OK")
