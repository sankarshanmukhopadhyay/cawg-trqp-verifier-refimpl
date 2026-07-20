#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys
root=Path(__file__).resolve().parents[1]
required=["README.md","LICENSE","CHANGELOG.md","ROADMAP.md","GOVERNANCE.md","CONTRIBUTING.md","SECURITY.md","CODE_OF_CONDUCT.md","CITATION.cff","QUICKSTART.md","data/repository-metadata.yaml","docs/trqp-adoption-path.md","docs/cawg-input-contract.md","docs/api-call-catalogue.md","api/openapi.json","docs/presentation.md","assets/presentations/cawg-trqp-explainer-v2.pdf","assets/presentations/cawg-trqp-explainer-v2-cover.png","assets/presentations/manifest.json"]
errors=[]
for rel in required:
    if not (root/rel).is_file(): errors.append(f"missing required flagship artifact: {rel}")

manifest_path=root/'assets/presentations/manifest.json'
if manifest_path.is_file():
    try:
        manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        for path_key, digest_key in [('path','sha256'),('cover_path','cover_sha256')]:
            artifact=root/manifest[path_key]
            if not artifact.is_file():
                errors.append(f"presentation manifest references missing artifact: {manifest[path_key]}")
                continue
            actual=hashlib.sha256(artifact.read_bytes()).hexdigest()
            if actual != manifest[digest_key]:
                errors.append(f"presentation checksum mismatch: {manifest[path_key]}")
        if manifest.get('implementation_version') != 'v0.17.0':
            errors.append('presentation implementation version is not aligned with repository v0.17.0')
        if manifest.get('status') != 'non-normative':
            errors.append('presentation authority status must be non-normative')
    except (KeyError, json.JSONDecodeError) as exc:
        errors.append(f"invalid presentation manifest: {exc}")

readme=(root/'README.md').read_text(encoding='utf-8')
for marker in ['Portfolio tier','Validation','Evidence output','Governance authority']:
    if marker not in readme: errors.append(f"README missing status contract marker: {marker}")
for md in root.rglob('*.md'):
    text=md.read_text(encoding='utf-8',errors='replace')
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
        t=target.split('#',1)[0].strip()
        if not t or '://' in t or t.startswith(('mailto:','data:','#')): continue
        dest=(md.parent/t).resolve()
        try: dest.relative_to(root.resolve())
        except ValueError: continue
        if not dest.exists(): errors.append(f"broken local link: {md.relative_to(root)} -> {target}")
if errors:
    print('Flagship repository validation failed:')
    for e in sorted(set(errors)): print(f'- {e}')
    sys.exit(1)
print('Flagship repository contract: PASS')
