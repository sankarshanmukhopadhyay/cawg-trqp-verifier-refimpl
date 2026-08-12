#!/usr/bin/env python3
"""Validate Mermaid coverage and basic fence integrity for indexed walkthrough docs."""
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/"docs"/"sections"/"walkthroughs-index.md"
LINK_RE=re.compile(r"\]\((\.\./(?:workflows/[^)]+|video-verification-walkthrough\.md))\)")
errors=[]
index_text=INDEX.read_text(encoding="utf-8")
linked=[]
for relative in LINK_RE.findall(index_text):
    path=(INDEX.parent/relative).resolve()
    if path not in linked: linked.append(path)
if not linked: errors.append("walkthrough index contains no walkthrough links")
for path in linked:
    rel=path.relative_to(ROOT)
    if not path.is_file(): errors.append(f"{rel}: document is missing"); continue
    text=path.read_text(encoding="utf-8")
    openings=text.count("```mermaid"); fences=text.count("```")
    if openings < 1: errors.append(f"{rel}: missing Mermaid diagram")
    if fences % 2: errors.append(f"{rel}: unbalanced fenced code blocks")
    if "## At-a-glance governance flow" not in text: errors.append(f"{rel}: missing standard at-a-glance flow heading")
    if "Operational assurance contract" not in text: errors.append(f"{rel}: missing operational assurance contract")
    for block in re.findall(r"```mermaid\s*\n(.*?)```",text,flags=re.S):
        first=next((line.strip() for line in block.splitlines() if line.strip()),"")
        if not (
            first.startswith("flowchart ")
            or first == "sequenceDiagram"
            or first in {"stateDiagram", "stateDiagram-v2"}
            or first.startswith("graph ")
        ):
            errors.append(f"{rel}: unsupported Mermaid diagram opening {first!r}")
if errors:
    print("walkthrough diagrams: FAIL")
    for error in errors: print(f"- {error}")
    sys.exit(1)
print(f"walkthrough diagrams: {len(linked)} indexed documents OK")
