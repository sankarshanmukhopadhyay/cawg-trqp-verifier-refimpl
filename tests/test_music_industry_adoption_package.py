import json
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples/music-industry"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(schema_name, example_name):
    schema = load_json(ROOT / "schemas" / schema_name)
    instance = load_json(EXAMPLES / example_name)
    jsonschema.Draft202012Validator(
        schema, format_checker=jsonschema.FormatChecker()
    ).validate(instance)


def test_music_cawg_signals_conform_to_generic_handoff_schema():
    validate("cawg-trqp-integration-signal.schema.json", "cawg-integration-signal.json")
    validate("cawg-trqp-integration-signal.schema.json", "ai-use-declaration-signal.json")


def test_music_authorization_records_conform_to_sector_schema():
    validate("music-industry-authorization-record.schema.json", "authorization-record.json")
    validate("music-industry-authorization-record.schema.json", "revoked-authorization-record.json")


def test_music_api_examples_conform_to_http_contract_schemas():
    validate("authorization-request.schema.json", "authorization-request.json")
    validate("authorization-response.schema.json", "authorization-response.json")
    validate("authorization-response.schema.json", "scope-mismatch-authorization-response.json")
    validate("recognition-request.schema.json", "recognition-request.json")
    validate("recognition-response.schema.json", "recognition-response.json")


def test_music_pilot_readiness_matrix_is_machine_readable():
    matrix = yaml.safe_load(
        (ROOT / "conformance/music-industry-pilot-readiness.yaml").read_text(encoding="utf-8")
    )
    assert matrix["profile"] == "recorded-music-distribution-pilot"
    assert matrix["authority_status"] == "non-normative-reference-profile"
    assert len(matrix["readiness_gates"]) >= 10
    owners = {gate["owner"] for gate in matrix["readiness_gates"]}
    assert "cawg-implementation-team" in owners
    assert "appeal-authority" in owners


def test_music_docs_keep_named_bodies_illustrative():
    landing = (ROOT / "docs/industry-adoption/index.md").read_text(encoding="utf-8")
    assert "do not imply endorsement" in landing
    playbook = (ROOT / "docs/industry-adoption/cawg-implementation-playbook.md").read_text(encoding="utf-8")
    for marker in [
        "What CAWG must undertake",
        "Mandatory CAWG failure behavior",
        "Implementation evidence checklist",
        "Minimum test matrix",
    ]:
        assert marker in playbook
