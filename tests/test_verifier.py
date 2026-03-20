from pathlib import Path
from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.snapshot import SnapshotStore
from cawg_trqp_refimpl.verifier import Verifier


def test_standard_verifier():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_minimal.json"), "did:web:media-registry.example")
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(req, profile="standard")
    assert result.trust_outcome == "trusted"


def test_edge_verifier():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_minimal.json"), "did:web:media-registry.example")
    verifier = Verifier(snapshot=SnapshotStore(Path("data/snapshot.json")))
    result = verifier.verify(req, profile="edge")
    assert result.trust_outcome == "trusted_cached"


def test_blocked_entity_rejected():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_blocked.json"), "did:web:media-registry.example")
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(req, profile="standard")
    assert result.trust_outcome == "rejected"
    assert result.actor_authorization == "not_authorized"
