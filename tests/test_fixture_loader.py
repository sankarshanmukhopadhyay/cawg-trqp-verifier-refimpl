from pathlib import Path
from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture


def test_fixture_loader():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_minimal.json"), "did:web:media-registry.example")
    assert req.entity_id == "did:web:publisher.example"
    assert req.action == "publish"
    assert req.resource == "cawg:news-content"
