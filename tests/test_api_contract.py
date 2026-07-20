import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def test_openapi_operation_inventory_is_complete():
    spec=load("api/openapi.json")
    actual={(method,path) for path,item in spec["paths"].items() for method in item if method in {"get","post"}}
    assert actual == {
        ("get", "/health"),
        ("post", "/trqp/authorization"),
        ("post", "/trqp/recognition"),
        ("post", "/trqp/gateway/authorization"),
        ("post", "/trqp/verify"),
        ("post", "/trqp/audit-bundle"),
    }

def test_canonical_payload_examples_validate():
    pairs=[
      ("schemas/authorization-request.schema.json","examples/api/authorization-request.json"),
      ("schemas/authorization-response.schema.json","examples/api/authorization-response.json"),
      ("schemas/recognition-request.schema.json","examples/api/recognition-request.json"),
      ("schemas/recognition-response.schema.json","examples/api/recognition-response.json"),
      ("schemas/gateway-authorization-response.schema.json","examples/api/gateway-authorization-response.json"),
      ("schemas/verification-result.schema.json","examples/api/verification-response.json"),
      ("schemas/audit-bundle.schema.json","examples/api/audit-bundle-response.json"),
    ]
    registry={}
    for schema_path,_ in pairs:
        schema=load(schema_path)
        Draft202012Validator.check_schema(schema)
        registry[schema_path]=schema
    # schemas without relative refs validate directly; gateway is exercised by HTTP tests and contract checker
    for schema_path,example_path in pairs:
        if schema_path.endswith("gateway-authorization-response.schema.json"):
            continue
        Draft202012Validator(registry[schema_path]).validate(load(example_path))
