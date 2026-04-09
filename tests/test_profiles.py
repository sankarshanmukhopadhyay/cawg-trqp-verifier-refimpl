from pathlib import Path

import pytest

from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture
from cawg_trqp_refimpl.profile import load_profile, VerificationProfileError
from cawg_trqp_refimpl.verifier import Verifier



def test_builtin_profile_loads_with_controls():
    profile = load_profile("high_assurance")
    assert profile.base_profile == "high_assurance"
    assert profile.controls["freshness"]["require_live"] is True
    assert profile.controls["evidence"]["require_attestation"] is True



def test_overlay_application_updates_profile_controls():
    profile = load_profile("standard", overlays=["evidence_attested", "freshness_strict"])
    assert profile.controls["evidence"]["require_attestation"] is True
    assert profile.controls["freshness"]["require_live"] is True
    assert profile.controls["failure"]["network_failure"] == "fail_closed"
    assert profile.overlays == ["evidence_attested", "freshness_strict"]



def test_unknown_profile_raises_validation_error():
    with pytest.raises(VerificationProfileError):
        load_profile("definitely-not-a-real-profile")



def test_fail_closed_profile_rejects_service_unavailable():
    request = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_minimal.json"), "did:web:media-registry.example")
    verifier = Verifier(service=None)
    result = verifier.verify(request, profile=load_profile("high_assurance"))
    assert result.trust_outcome == "rejected"
    assert result.policy_freshness == "service_unavailable"



def test_fail_open_profile_defers_service_unavailable():
    request = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_minimal.json"), "did:web:media-registry.example")
    verifier = Verifier(service=None)
    result = verifier.verify(request, profile=load_profile("standard"))
    assert result.trust_outcome == "deferred"
    assert result.policy_freshness == "service_unavailable"
