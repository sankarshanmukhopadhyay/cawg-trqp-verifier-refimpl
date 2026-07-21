#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, sys
root=Path(__file__).resolve().parents[1]
required=["README.md","LICENSE","CHANGELOG.md","ROADMAP.md","GOVERNANCE.md","CONTRIBUTING.md","SECURITY.md","CODE_OF_CONDUCT.md","CITATION.cff","QUICKSTART.md","data/repository-metadata.yaml","docs/trqp-adoption-path.md","docs/cawg-input-contract.md","docs/cawg-trqp-integration-enablement.md","docs/api-call-catalogue.md","schemas/cawg-trqp-integration-signal.schema.json","conformance/cawg-trqp-readiness-matrix.yaml","api/openapi.json","docs/presentation.md","assets/presentations/cawg-trqp-explainer-v2.pdf","assets/presentations/cawg-trqp-explainer-v2-cover.png","assets/presentations/manifest.json","docs/scalability-and-performance.md","docs/cache-freshness-and-revocation.md","docs/high-volume-deployment-profile.md","schemas/cache-policy.schema.json","schemas/performance-evidence.schema.json","benchmarks/README.md","benchmarks/benchmark_verifier.py","benchmarks/benchmark_http.py","benchmarks/scenarios.yaml","benchmarks/expected-thresholds.yaml","docs/industry-adoption/index.md","docs/industry-adoption/industry-body-decision-brief.md","docs/industry-adoption/music-industry-application-profile.md","docs/industry-adoption/cawg-implementation-playbook.md","docs/industry-adoption/music-industry-pilot-blueprint.md","docs/workflows/authorized-music-distribution.md","schemas/music-industry-authorization-record.schema.json","examples/music-industry/cawg-integration-signal.json","conformance/music-industry-pilot-readiness.yaml"]
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


# GitHub Pages/Just the Docs integrity checks. Every rendered documentation
# page must opt into the theme layout, and every declared parent must resolve
# to a navigation node that advertises children.
doc_pages = sorted((root / "docs").rglob("*.md"))
nav_nodes = {}
page_front_matter = {}
front_matter_pattern = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

for page in doc_pages:
    rel = page.relative_to(root)
    text = page.read_text(encoding="utf-8", errors="replace")
    match = front_matter_pattern.match(text)
    if not match:
        errors.append(f"GitHub Pages document missing front matter: {rel}")
        continue

    fields = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    page_front_matter[rel] = fields

    if fields.get("layout") != "default":
        errors.append(f"GitHub Pages document must use layout default: {rel}")

    title = fields.get("title")
    if title and fields.get("has_children", "").lower() == "true":
        nav_nodes[title] = rel

for rel, fields in page_front_matter.items():
    parent = fields.get("parent")
    if parent and parent not in nav_nodes:
        errors.append(f"GitHub Pages document has unresolved navigation parent '{parent}': {rel}")

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
