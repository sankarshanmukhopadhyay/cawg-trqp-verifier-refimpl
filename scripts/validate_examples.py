#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    'audit_bundle': json.loads((ROOT / 'schemas' / 'audit-bundle.schema.json').read_text(encoding='utf-8')),
    'verification_profile': json.loads((ROOT / 'schemas' / 'verification-profile.schema.json').read_text(encoding='utf-8')),
    'verification_request': json.loads((ROOT / 'schemas' / 'verification-request.schema.json').read_text(encoding='utf-8')),
    'verification_result': json.loads((ROOT / 'schemas' / 'verification-result.schema.json').read_text(encoding='utf-8')),
}

def iter_validation_targets() -> list[tuple[str, Path, object]]:
    targets: list[tuple[str, Path, object]] = []
    for path in sorted((ROOT / 'examples').rglob('*.json')):
        rel = path.relative_to(ROOT)
        if rel.parts[:2] == ('examples', 'fixtures'):
            continue
        data = json.loads(path.read_text(encoding='utf-8'))
        if path.name in {'exported_audit_bundle.json', 'exported_audit_bundle.signed.json', 'reproducibility_bundle_standard.json'}:
            targets.append(('audit_bundle', rel, data))
        elif path.parent.name == 'expected':
            targets.append(('verification_result', rel, data))
        elif path.name.startswith('benchmark_') or path.name in {'verification_request.json', 'interoperability_vector_gateway.json'}:
            targets.append(('verification_request', rel, data))
        elif path.name == 'interoperability_vector_multi_authority.json':
            for idx, item in enumerate(data.get('vectors', [])):
                targets.append(('verification_request', Path(f'{rel}:vectors[{idx}]'), item))
    for path in sorted((ROOT / 'fixtures' / 'profile-bound').glob('*/request.json')):
        targets.append(('verification_request', path.relative_to(ROOT), json.loads(path.read_text(encoding='utf-8'))))
    for path in sorted((ROOT / 'fixtures' / 'profile-bound').glob('*/resolved_profile.json')):
        targets.append(('verification_profile', path.relative_to(ROOT), json.loads(path.read_text(encoding='utf-8'))))
    for path in sorted((ROOT / 'fixtures' / 'profile-bound').glob('*/expected_result.json')):
        targets.append(('verification_result', path.relative_to(ROOT), json.loads(path.read_text(encoding='utf-8'))))
    return targets

def main() -> int:
    failures: list[str] = []
    checked = 0
    for schema_name, rel_path, data in iter_validation_targets():
        validator = Draft202012Validator(SCHEMAS[schema_name])
        errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
        if errors:
            for err in errors:
                pointer = '/'.join(str(p) for p in err.path) or '<root>'
                failures.append(f'{rel_path}: {pointer}: {err.message}')
        checked += 1
    if failures:
        print('validate_examples.py: FAIL')
        for failure in failures:
            print(f' - {failure}')
        return 1
    print(f'validate_examples.py: {checked}/{checked} OK')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
