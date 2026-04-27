import json
from pathlib import Path

from cawg_trqp_refimpl.audit import build_audit_bundle
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.profile import load_profile
from cawg_trqp_refimpl.replay import replay_audit_bundle
from cawg_trqp_refimpl.verifier import Verifier


def _request() -> VerificationRequest:
    return VerificationRequest(**json.loads(Path("examples/verification_request.json").read_text(encoding="utf-8")))


def test_transport_constraint_rejects_insufficient_integrity_for_high_assurance_overlay():
    profile = load_profile({
        "id": "strict_transport_test",
        "base_profile": "standard",
        "controls": {
            "transport": {
                "mode": "http",
                "integrity": "signed",
                "availability_requirement": "required"
            }
        },
        "overlays": [],
        "source": "inline"
    })
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json"), transport_integrity="tls"))
    result = verifier.verify(_request(), profile=profile)
    assert result.verification_mode == "transport_guardrail"
    assert result.policy_freshness == "transport_violation"
    assert result.policy_evidence["transport"]["satisfied"] is False


def test_revocation_freshness_warn_path_keeps_verification_running():
    profile = load_profile({
        "id": "warn_revocation_test",
        "base_profile": "standard",
        "controls": {
            "transport": {
                "mode": "http",
                "integrity": "tls",
                "availability_requirement": "best_effort"
            },
            "revocation": {
                "mode": "delta",
                "hard_fail": False,
                "max_age_seconds": 1,
                "enforcement": "warn",
                "delta_channel_required": False
            }
        },
        "overlays": [],
        "source": "inline"
    })
    stale_path = Path("tests/tmp_stale_revocations.json")
    stale_path.write_text(json.dumps({
        "revoked_entities": [],
        "policy_epoch": "2026-Q1",
        "issued_at": "2020-01-01T00:00:00Z",
        "channel": "delta"
    }), encoding="utf-8")
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), stale_path))
    result = verifier.verify(_request(), profile=profile)
    stale_path.unlink()
    assert result.trust_outcome == "trusted"
    assert result.policy_freshness == "stale_but_warned"
    assert result.policy_evidence["revocation_status"]["freshness_ok"] is False


def test_replay_bundle_carries_transport_and_revocation_contract():
    verifier = Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))
    result = verifier.verify(_request(), profile="standard")
    bundle = build_audit_bundle(
        _request(),
        result,
        profile="standard",
        exported_at="2026-03-31T00:00:00Z",
        policy_path="data/policies.json",
        revocation_path="data/revocations.json",
    ).to_dict()
    assert "transport_metadata" in bundle["replay_inputs"]
    assert "revocation_status" in bundle["replay_inputs"]
    assert bundle["replay_inputs"]["replay_contract"]["revocation_freshness_evaluated"] is True

    report = replay_audit_bundle(bundle)
    assert report.matches is True


def test_canonical_fixture_manifest_is_complete():
    manifest = json.loads(Path("fixtures/profile-bound/standard-v1/manifest.json").read_text(encoding="utf-8"))
    assert manifest["fixture_id"] == "standard-v1"
    assert manifest["inputs"]["request"] == "request.json"
    assert Path("fixtures/profile-bound/standard-v1/pinned_feeds/policies.json").exists()
    assert Path("fixtures/profile-bound/standard-v1/pinned_feeds/revocations.json").exists()
