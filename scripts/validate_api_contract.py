#!/usr/bin/env python3
"""Validate the API operation inventory, referenced schemas, and canonical examples."""
from __future__ import annotations
import json
from pathlib import Path
import sys
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "api" / "openapi.json"
EXPECTED = {
    ("get", "/health"),
    ("post", "/trqp/authorization"),
    ("post", "/trqp/recognition"),
    ("post", "/trqp/gateway/authorization"),
    ("post", "/trqp/verify"),
    ("post", "/trqp/audit-bundle"),
}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def local_path(base: Path, value: str) -> Path:
    return (base.parent / value).resolve()

def main() -> int:
    errors=[]
    spec=load(SPEC)
    operations={(method,path) for path,item in spec.get("paths",{}).items() for method in item if method in {"get","post","put","patch","delete"}}
    if operations != EXPECTED:
        errors.append(f"operation inventory mismatch: expected {sorted(EXPECTED)}, got {sorted(operations)}")
    operation_ids=[]
    for path,item in spec.get("paths",{}).items():
        for method,op in item.items():
            if method not in {"get","post","put","patch","delete"}: continue
            operation_ids.append(op.get("operationId"))
            for node in walk(op):
                if isinstance(node,dict) and isinstance(node.get("$ref"),str) and node["$ref"].startswith("../"):
                    target=local_path(SPEC,node["$ref"])
                    if not target.is_file(): errors.append(f"missing schema ref for {method.upper()} {path}: {node['$ref']}")
                    else:
                        try: Draft202012Validator.check_schema(load(target))
                        except Exception as exc: errors.append(f"invalid schema {target.relative_to(ROOT)}: {exc}")
                if isinstance(node,dict) and isinstance(node.get("externalValue"),str) and node["externalValue"].startswith("../"):
                    target=local_path(SPEC,node["externalValue"])
                    if not target.is_file(): errors.append(f"missing example for {method.upper()} {path}: {node['externalValue']}")
                    else:
                        try: load(target)
                        except Exception as exc: errors.append(f"invalid JSON example {target.relative_to(ROOT)}: {exc}")
    if len(operation_ids) != len(set(operation_ids)) or None in operation_ids:
        errors.append("operationId values must be present and unique")
    if errors:
        print("API contract validation failed:")
        for error in errors: print(f"- {error}")
        return 1
    print(f"API contract: PASS ({len(operations)} operations)")
    return 0

def walk(value):
    yield value
    if isinstance(value,dict):
        for child in value.values(): yield from walk(child)
    elif isinstance(value,list):
        for child in value: yield from walk(child)

if __name__ == "__main__":
    sys.exit(main())
