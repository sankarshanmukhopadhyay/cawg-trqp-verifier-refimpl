from pathlib import Path

from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture
from cawg_trqp_refimpl.manifest_parser import CAWGManifestParser


def test_fixture_loader():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_minimal.json"), "did:web:media-registry.example")
    assert req.entity_id == "did:web:publisher.example"
    assert req.action == "publish"
    assert req.resource == "cawg:news-content"


def test_c2pa_loader():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_c2pa.json"), "did:web:media-registry.example")
    assert req.entity_id == "did:web:publisher.example"
    assert req.context["credential_type"] == "vc:creator-identity"


def test_manifest_validator_reports_mode():
    result = CAWGManifestParser.validate_fixture(Path("examples/fixtures/cawg_manifest_c2pa.json"))
    assert result["valid"] is True
    assert result["parser_mode"] == "c2pa_json"
