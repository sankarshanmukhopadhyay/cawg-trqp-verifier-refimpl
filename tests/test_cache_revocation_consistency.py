"""Adversarial cache/revocation consistency contracts (issue #105)."""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from cawg_trqp_refimpl import mock_service
from cawg_trqp_refimpl.audit import build_audit_bundle
from cawg_trqp_refimpl.http_service import HTTPTRQPService
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.replay import replay_audit_bundle
from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.profile import load_profile
from cawg_trqp_refimpl.verifier import Verifier


def _setup():
    service = MockTRQPService(Path("data/policies.json"), Path("data/revocations.json"))
    service.revocations["issued_at"] = datetime.now(timezone.utc).isoformat()
    request = load_manifest_fixture(
        Path("examples/fixtures/cawg_manifest_minimal.json"),
        "did:web:media-registry.example",
    )
    return service, request


def _strict_cached_profile():
    # Require fresh revocation evidence while retaining cache-assisted authorization.
    # This isolates the freshness contract from high_assurance's require_live control.
    profile = load_profile("standard").to_dict()
    profile["id"] = "strict-revocation-cached"
    profile["controls"]["revocation"]["enforcement"] = "fail"
    return profile


@pytest.mark.parametrize("issued_at", [None, "not-a-timestamp", "2099-01-01T00:00:00Z"])
def test_required_revocation_freshness_rejects_unusable_issue_time(issued_at):
    service, request = _setup()
    if issued_at is None:
        service.revocations.pop("issued_at", None)
    else:
        service.revocations["issued_at"] = issued_at
    result = Verifier(service=service).verify(request, profile=_strict_cached_profile())
    assert result.trust_outcome == "rejected"
    assert result.policy_freshness == "revocation_stale"
    assert result.policy_evidence["revocation_status"]["freshness_ok"] is False


def test_cache_revalidates_authorization_when_revocation_epoch_changes():
    service, request = _setup()
    verifier = Verifier(service=service)
    first = verifier.verify(request, profile="standard")
    assert first.actor_authorization == "authorized"
    second = verifier.verify(request, profile="standard")
    assert second.policy_evidence["cache"]["authorization"]["cache_hit"] is True

    # A newer observed epoch explicitly revokes the previously cached actor.
    service.revocations["policy_epoch"] = "2026-Q2"
    service.revocations["revoked_entities"].append(request.entity_id)
    updated = verifier.verify(request, profile="standard")
    assert updated.actor_authorization == "not_authorized"
    assert updated.trust_outcome == "rejected"
    assert updated.policy_evidence["cache"]["authorization"]["cache_hit"] is False


def test_cache_revalidates_recognition_when_epoch_changes():
    service, request = _setup()
    verifier = Verifier(service=service)
    initial = verifier.verify(request, profile="standard")
    assert initial.issuer_recognition == "recognized"
    again = verifier.verify(request, profile="standard")
    assert again.policy_evidence["cache"]["recognition"]["cache_hit"] is True

    service.revocations["policy_epoch"] = "2026-Q2"
    service.data["recognition"][0]["policy_epoch"] = "2026-Q2"
    service.data["recognition"][0]["recognized"] = False
    updated = verifier.verify(request, profile="standard")
    assert updated.issuer_recognition != "recognized"
    assert updated.policy_evidence["cache"]["recognition"]["cache_hit"] is False


def test_revocation_feed_age_boundary_is_explicit():
    service, request = _setup()
    service.revocations["issued_at"] = (
        datetime.now(timezone.utc) - timedelta(days=5)
    ).isoformat()
    result = Verifier(service=service).verify(request, profile=_strict_cached_profile())
    assert result.trust_outcome == "rejected"
    assert result.policy_evidence["revocation_status"]["freshness_ok"] is False


def test_http_consumer_does_not_reuse_authorization_after_observed_epoch_change():
    service = HTTPTRQPService(
        policy_path=Path("data/policies.json"),
        revocation_path=Path("data/revocations.json"),
    )
    service.app.config["TESTING"] = True
    service.mock_service.revocations["issued_at"] = datetime.now(timezone.utc).isoformat()
    client = service.app.test_client()
    payload = json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8"))

    initial = client.post("/trqp/verify", json=payload)
    assert initial.status_code == 200
    assert initial.get_json()["actor_authorization"] == "authorized"
    cached = client.post("/trqp/verify", json=payload)
    assert cached.get_json()["policy_evidence"]["cache"]["authorization"]["cache_hit"] is True

    service.mock_service.revocations["policy_epoch"] = "2026-Q2"
    service.mock_service.revocations["revoked_entities"].append(payload["entity_id"])
    after = client.post("/trqp/verify", json=payload)
    assert after.status_code == 200
    body = after.get_json()
    assert body["actor_authorization"] == "not_authorized"
    assert body["trust_outcome"] == "rejected"
    assert body["policy_evidence"]["cache"]["authorization"]["cache_hit"] is False


def test_fresh_pinned_replay_still_matches_after_freshness_hardening(tmp_path):
    # Unlike the archived bundles, this fixture has an issuance time that
    # precedes its explicitly pinned evaluation time.
    policy_path = tmp_path / "policies.json"
    revocation_path = tmp_path / "revocations.json"
    policy_path.write_text(Path("data/policies.json").read_text(encoding="utf-8"))
    revocations = json.loads(Path("data/revocations.json").read_text(encoding="utf-8"))
    revocations["issued_at"] = "2026-11-24T00:59:30Z"
    revocation_path.write_text(json.dumps(revocations), encoding="utf-8")

    class PinnedClock(datetime):
        @classmethod
        def now(cls, tz=None):
            instant = datetime(2026, 11, 24, 1, 0, tzinfo=timezone.utc)
            return instant if tz is None else instant.astimezone(tz)

    request = VerificationRequest(**json.loads(
        Path("examples/verification_request.json").read_text(encoding="utf-8")
    ))
    with patch.object(mock_service, "datetime", PinnedClock):
        verifier = Verifier(service=MockTRQPService(
            policy_path, revocation_path, trust_anchors_path=None
        ))
        result = verifier.verify(request, profile="standard")
        assert result.policy_freshness == "fresh"
        bundle = build_audit_bundle(
            request, result,
            profile="standard",
            policy_path=policy_path,
            revocation_path=revocation_path,
        ).to_dict()
        replayed = replay_audit_bundle(bundle, trusted_root=tmp_path)
    assert replayed.matches is True, replayed.differences
