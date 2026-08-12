#!/usr/bin/env python3
"""Validate reader-facing quality structure for indexed walkthrough documentation."""
from pathlib import Path
import re, sys

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'docs'/'sections'/'walkthroughs-index.md'
LINK_RE=re.compile(r"\]\((\.\./(?:workflows/[^)]+|video-verification-walkthrough\.md))\)")

errors=[]
text=INDEX.read_text(encoding='utf-8')
linked=[]
for relative in LINK_RE.findall(text):
    p=(INDEX.parent/relative).resolve()
    if p not in linked: linked.append(p)

if not linked:
    errors.append('walkthrough index contains no walkthrough links')

required_exact=[
    'Plain-language summary',
    'At-a-glance governance flow',
    'Cross-functional interaction view',
    'Governed decision state model',
    'Roles in the workflow',
    'What evidence is produced',
    'What can be tested',
    'Why this improves adoption',
    'Governance interpretation',
    'Operational assurance contract',
]

for p in linked:
    rel=p.relative_to(ROOT)
    if not p.is_file():
        errors.append(f'{rel}: document is missing')
        continue
    body=p.read_text(encoding='utf-8')
    headings=set(re.findall(r'^##\s+(.+?)\s*$',body,re.M))
    for heading in required_exact:
        if heading not in headings:
            errors.append(f'{rel}: missing quality section {heading!r}')

    why_ok=any(h.lower().startswith('why ') and h != 'Why this improves adoption' and h != 'Why this matters' for h in headings)
    if not why_ok:
        errors.append(f'{rel}: missing scenario-specific why-governance section')

    mapping_ok=('System components mapped to workflow concepts' in headings or
                'Agent governance concepts mapped to verifier controls' in headings or
                'System components mapped to contest concepts' in headings)
    if not mapping_ok:
        errors.append(f'{rel}: missing domain-to-verifier concept mapping')

    # Depth is a guardrail, not a target. It catches accidental replacement with skeletal templates.
    words=len(re.findall(r'\b\w+\b',body))
    if words < 1200:
        errors.append(f'{rel}: walkthrough is too shallow for the quality baseline ({words} words; minimum 1200)')

    if '**' not in body:
        errors.append(f'{rel}: missing emphasized bounded decision or reader-facing key point')

if errors:
    print('walkthrough quality: FAIL')
    for e in errors: print(f'- {e}')
    sys.exit(1)
print(f'walkthrough quality: {len(linked)} indexed documents satisfy the structural/depth baseline')
