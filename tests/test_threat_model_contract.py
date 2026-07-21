from pathlib import Path
import json, yaml
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]

def load_yaml(path):
    return yaml.safe_load((ROOT/path).read_text(encoding="utf-8"))

def schema(name):
    return json.loads((ROOT/"schemas"/name).read_text(encoding="utf-8"))

def test_adversary_catalog_valid():
    validator=Draft202012Validator(schema("adversary-profile.schema.json"))
    items=load_yaml("governance/adversary-catalog.yaml")["adversaries"]
    assert len(items)>=10
    for item in items: validator.validate(item)

def test_threat_register_has_complete_controls_and_evidence():
    validator=Draft202012Validator(schema("threat-record.schema.json"))
    threats=load_yaml("governance/threat-register.yaml")["threats"]
    assert len(threats)>=6
    for threat in threats:
        validator.validate(threat)
        if threat["impact"] in {"critical","high"}:
            assert threat["controls"]["preventive"]
            assert threat["controls"]["detective"]
            assert threat["controls"]["recovery"]
            assert threat["evidence"]

def test_attack_surfaces_are_covered_by_threats():
    surfaces={x["id"] for x in load_yaml("governance/attack-surface.yaml")["surfaces"]}
    covered={s for t in load_yaml("governance/threat-register.yaml")["threats"] for s in t["surface_ids"]}
    assert surfaces <= covered

def test_abuse_cases_validate():
    validator=Draft202012Validator(schema("abuse-case.schema.json"))
    for item in load_yaml("governance/abuse-case-register.yaml")["abuse_cases"]: validator.validate(item)

def test_residual_risks_have_owner_and_expiry():
    validator=Draft202012Validator(schema("residual-risk.schema.json"), format_checker=Draft202012Validator.FORMAT_CHECKER)
    for item in load_yaml("governance/residual-risk-register.yaml")["risks"]:
        validator.validate(item)
        assert item["accepted_by"] and item["acceptance_expiry"]

def test_canonical_threat_examples_validate():
    validator=Draft202012Validator(schema("threat-record.schema.json"))
    for path in sorted((ROOT/"examples/threats").glob("*.yaml")): validator.validate(yaml.safe_load(path.read_text()))

def test_threat_docs_are_pages_ready_and_diagram_rich():
    pages=sorted((ROOT/"docs/threats-and-risks").glob("*.md"))
    assert len(pages)>=12
    diagrams=0
    for page in pages:
        text=page.read_text()
        assert text.startswith("---\n")
        assert "layout: default" in text.split("---",2)[1]
        diagrams += text.count("```mermaid")
    assert diagrams>=12
