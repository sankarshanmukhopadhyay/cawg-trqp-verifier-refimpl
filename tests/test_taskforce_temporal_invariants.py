"""Temporal non-elevation regression contract for the experimental evaluator.

All timestamps are caller-supplied. The results below are simulated temporal
logic, not verified historical authority or trusted revocation evidence.
"""
from copy import deepcopy

from cawg_trqp_refimpl.experimental_delegated_creator import evaluate
from test_experimental_delegated_creator import case


def test_later_withdrawal_preserves_only_simulated_historical_result():
    c = case()
    c["chain"][0]["revoked_at"] = "2026-10-24T00:00:00Z"
    c["evaluated_at"] = "2026-10-25T00:00:00Z"
    result = evaluate(c)
    assert result["historical_authority"] == "authorized"
    assert result["current_authority"] == "denied"
    assert result["assured_authority"] == "indeterminate"
    assert result["evidence_provenance"]["signing_time"] == "caller_supplied_untrusted"


def test_expired_delegation_retains_historical_simulation_not_current_permission():
    c = case()
    c["evaluated_at"] = "2026-11-01T00:00:00Z"
    result = evaluate(c)
    assert result["historical_authority"] == "authorized"
    assert result["current_authority"] == "denied"
    assert result["assured_authority"] == "indeterminate"


def test_signature_at_revocation_boundary_is_denied():
    c = case()
    c["chain"][0]["revoked_at"] = c["signed_at"]
    assert evaluate(c)["historical_authority"] == "denied"


def test_signature_at_expiry_boundary_is_denied():
    c = case()
    c["signed_at"] = c["chain"][0]["not_after"]
    assert evaluate(c)["historical_authority"] == "denied"


def test_invalid_or_missing_evidence_never_becomes_assured():
    for mutation in ("absent", "tampered", "claimed_credential"):
        c = deepcopy(case())
        if mutation == "absent":
            c["links"] = []
        elif mutation == "tampered":
            c["links"][0]["content"] = {"agreement": "replaced"}
        else:
            c["chain"][0]["credential_verified"] = True
        result = evaluate(c)
        assert result["assured_authority"] == "indeterminate"
        assert result["assured_coverage"] == "unverified"
        assert result["evidence_provenance"]["signing_time"] == "caller_supplied_untrusted"
