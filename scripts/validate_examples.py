#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    'audit_bundle': json.loads((ROOT / 'schemas' / 'audit-bundle.schema.json').read_text(encoding='utf-8')),
    'verification_profile': json.loads((ROOT / 'schemas' / 'verification-profile.schema.json').read_text(encoding='utf-8')),
    'verification_request': json.loads((ROOT / 'schemas' / 'verification-request.schema.json').read_text(encoding='utf-8')),
    'verification_result': json.loads((ROOT / 'schemas' / 'verification-result.schema.json').read_text(encoding='utf-8')),
}

FILES = {
    'audit_bundle': [
        'examples/exported_audit_bundle.json',
        'examples/exported_audit_bundle.signed.json',
        'examples/reproducibility_bundle_standard.json',
    ],
    'verification_profile': [
        'fixtures/profile-bound/standard-v1/resolved_profile.json',
    ],
    'verification_request': [
        'examples/verification_request.json',
        'examples/benchmark_high_volume_request.json',
        'examples/benchmark_constrained_device_request.json',
        'examples/interoperability_vector_gateway.json',
        'fixtures/profile-bound/standard-v1/request.json',
    ],
    'verification_result': [
        'examples/expected/standard_result.json',
        'examples/expected/edge_result.json',
        'fixtures/profile-bound/standard-v1/expected_result.json',
    ],
}


def main() -> int:
    checked = 0
    failures: list[str] = []
    for schema_name, rel_paths in FILES.items():
        validator = Draft202012Validator(SCHEMAS[schema_name])
        for rel_path in rel_paths:
            path = ROOT / rel_path
            data = json.loads(path.read_text(encoding='utf-8'))
            errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
            if errors:
                for err in errors:
                    pointer = '/'.join(str(p) for p in err.path) or '<root>'
                    failures.append(f'{rel_path}: {pointer}: {err.message}')
            checked += 1

    multi_authority_path = ROOT / 'examples/interoperability_vector_multi_authority.json'
    multi_authority = json.loads(multi_authority_path.read_text(encoding='utf-8'))
    validator = Draft202012Validator(SCHEMAS['verification_request'])
    for idx, item in enumerate(multi_authority.get('vectors', [])):
        errors = sorted(validator.iter_errors(item), key=lambda err: list(err.path))
        if errors:
            for err in errors:
                pointer = '/'.join(str(p) for p in err.path) or '<root>'
                failures.append(f"examples/interoperability_vector_multi_authority.json:vectors[{idx}]: {pointer}: {err.message}")
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
