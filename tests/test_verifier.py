from datetime import datetime, timezone
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
    assert result.process_integrity == "verified_high"


def test_edge_verifier():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_minimal.json"), "did:web:media-registry.example")
    snapshot_time = datetime(2026, 8, 16, 12, 0, 0, tzinfo=timezone.utc)
    verifier = Verifier(
        snapshot=SnapshotStore(
            Path("data/snapshot.json"),
            Path("data/trust_anchors.json"),
            current_time=snapshot_time,
        )
    )
    result = verifier.verify(req, profile="edge")
    assert result.trust_outcome == "trusted_cached"
    assert result.policy_freshness == "snapshot_verified"
    assert result.process_integrity == "verified_high"
    assert result.policy_evidence["revocation_status"]["authority_state_age_seconds"] == 28800


def test_blocked_entity_rejected():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_blocked.json"), "did:web:media-registry.example")
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(req, profile="standard")
    assert result.trust_outcome == "rejected"
    assert result.actor_authorization == "not_authorized"


def test_c2pa_manifest_fixture_supported():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_c2pa.json"), "did:web:media-registry.example")
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(req, profile="standard")
    assert result.trust_outcome == "trusted"
    assert result.process_integrity in {"verified", "verified_high"}


def test_failed_process_proof_rejected():
    req = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_c2pa_pop_failed.json"), "did:web:media-registry.example")
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(req, profile="standard")
    assert result.actor_authorization == "authorized"
    assert result.process_integrity == "failed"
    assert result.trust_outcome == "rejected"
