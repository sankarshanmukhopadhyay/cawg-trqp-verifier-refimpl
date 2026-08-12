#!/usr/bin/env python3
"""Validate discoverability and minimum conformance structure of the agentic assurance overlay."""
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "sections" / "walkthroughs-index.md"
AGENT_INDEX = ROOT / "docs" / "agentic-ai" / "index.md"
ARCHETYPES = {
    "agent-content-producer",
    "agent-delegated-submitter",
    "agent-verifier-orchestrator",
}
REQUIRED_AGENT_DOCS = {
    "index.md",
    "agent-role-model.md",
    "delegation-and-authority.md",
    "agentic-verification-boundaries.md",
    "agentic-walkthrough-pattern.md",
}
errors=[]

for name in REQUIRED_AGENT_DOCS:
    path=ROOT/"docs"/"agentic-ai"/name
    if not path.is_file():
        errors.append(f"missing agentic assurance document: {path.relative_to(ROOT)}")

index_text=INDEX.read_text(encoding="utf-8")
if "Agentic AI Assurance" not in index_text:
    errors.append("walkthrough index does not link the Agentic AI Assurance model")

links=[]
for rel in re.findall(r"\]\((\.\./(?:workflows/[^)]+|video-verification-walkthrough\.md))\)", index_text):
    path=(INDEX.parent/rel).resolve()
    if path not in links: links.append(path)

sector_count=0
for path in links:
    if path.stem in ARCHETYPES:
        continue
    sector_count += 1
    text=path.read_text(encoding="utf-8")
    if "## Agentic AI Variant" not in text:
        errors.append(f"{path.relative_to(ROOT)}: missing Agentic AI Variant")
    for phrase in ("Agent role", "Principal", "Delegated authority", "Revocation", "Audit and redress"):
        if phrase not in text:
            errors.append(f"{path.relative_to(ROOT)}: agentic variant missing {phrase!r}")

for slug in sorted(ARCHETYPES):
    doc=ROOT/"docs"/"workflows"/(slug+".md")
    scenario=ROOT/"examples"/slug/"scenario.json"
    if not doc.is_file(): errors.append(f"missing agentic archetype doc: {doc.relative_to(ROOT)}")
    if not scenario.is_file(): errors.append(f"missing agentic archetype scenario: {scenario.relative_to(ROOT)}"); continue
    data=json.loads(scenario.read_text(encoding="utf-8"))
    outputs=set(data.get("evidence_outputs",[]))
    required={"decision_receipt","agent_identity","principal_reference","delegation_evidence","scope_evidence","replay_inputs"}
    missing=required-outputs
    if missing: errors.append(f"{scenario.relative_to(ROOT)}: missing agentic evidence outputs {sorted(missing)}")
    if f"../workflows/{slug}.md" not in index_text:
        errors.append(f"{slug}: archetype not discoverable from walkthrough index")

if sector_count < 1:
    errors.append("no sector walkthroughs discovered")

if errors:
    print("agentic assurance: FAIL")
    for e in errors: print(f"- {e}")
    sys.exit(1)
print(f"agentic assurance: {sector_count} sector variants + {len(ARCHETYPES)} executable archetypes OK")
