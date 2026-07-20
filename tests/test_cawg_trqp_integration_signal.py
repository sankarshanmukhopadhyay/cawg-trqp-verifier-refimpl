import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/cawg-trqp-integration-signal.schema.json").read_text())
VALID = ["valid-minimal.json", "valid-full.json"]
INVALID = ["missing-actor.json", "ambiguous-issuer.json", "unsupported-action.json"]


def load(name):
    return json.loads((ROOT / "examples/cawg-trqp" / name).read_text())


def test_valid_integration_signals():
    for name in VALID:
        jsonschema.Draft202012Validator(SCHEMA, format_checker=jsonschema.FormatChecker()).validate(load(name))


def test_negative_integration_signals_are_rejected():
    validator = jsonschema.Draft202012Validator(SCHEMA, format_checker=jsonschema.FormatChecker())
    for name in INVALID:
        assert list(validator.iter_errors(load(name))), f"{name} unexpectedly validated"


def test_readiness_matrix_is_machine_readable():
    import yaml
    matrix = yaml.safe_load((ROOT / "conformance/cawg-trqp-readiness-matrix.yaml").read_text())
    assert matrix["version"] == "0.1"
    assert matrix["authority_status"] == "non-normative-reference-profile"
    assert len(matrix["readiness_gates"]) >= 7
