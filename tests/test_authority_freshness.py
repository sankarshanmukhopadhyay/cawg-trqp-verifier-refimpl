from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture
from cawg_trqp_refimpl.profile import load_profile
from cawg_trqp_refimpl.snapshot import SnapshotStore
from cawg_trqp_refimpl.verifier import Verifier


def _request():
    return load_manifest_fixture(Path("examples/fixtures/cawg_manifest_minimal.json"), "did:web:media-registry.example")


def _stale_snapshot():
    return SnapshotStore(
        Path("data/snapshot.json"),
        Path("data/trust_anchors.json"),
        current_time=datetime(2026, 8, 18, 4, 0, tzinfo=timezone.utc),
    )


def test_stale_snapshot_defers_under_bounded_edge_profile_and_records_age_evidence():
    result = Verifier(snapshot=_stale_snapshot()).verify(_request(), profile="edge")
    assert result.trust_outcome == "deferred"
    assert result.policy_freshness == "authority_state_stale"
    evidence = result.policy_evidence["revocation_status"]
    assert evidence["authority_state_timestamp"] == "2026-08-16T04:00:00Z"
    assert evidence["authority_state_age_seconds"] > evidence["authority_state_max_age_seconds"]
    assert evidence["stale_disposition"] == "defer"


def test_stale_snapshot_can_be_fail_closed_for_consequential_edge_profile():
    profile = load_profile("edge").to_dict()
    profile["id"] = "edge-high-assurance"
    profile["controls"]["freshness"]["stale_disposition"] = "deny"
    result = Verifier(snapshot=_stale_snapshot()).verify(_request(), profile=profile)
    assert result.trust_outcome == "rejected"
    assert result.policy_evidence["revocation_status"]["freshness_ok"] is False


def test_cached_authority_state_is_bounded_by_profile_age_and_exposes_cache_evidence():
    from cawg_trqp_refimpl.cache import TTLCache
    from cawg_trqp_refimpl.mock_service import MockTRQPService

    cache = TTLCache()
    verifier = Verifier(
        service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")),
        cache=cache,
    )
    profile = load_profile("standard").to_dict()
    profile["id"] = "short-cache-age"
    profile["controls"]["freshness"]["max_age_seconds"] = 10
    profile["controls"]["freshness"]["stale_disposition"] = "defer"
    first = verifier.verify(_request(), profile=profile)
    assert first.trust_outcome == "trusted"

    for entry in cache.cache.values():
        entry.cached_at -= 20

    second = verifier.verify(_request(), profile=profile)
    assert second.trust_outcome == "deferred"
    assert second.policy_freshness == "authority_state_stale"
    assert second.policy_evidence["cache"]["stale_items"]
