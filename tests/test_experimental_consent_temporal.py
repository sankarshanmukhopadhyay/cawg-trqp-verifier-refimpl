"""Temporal consent claim semantics remain distinct from historical authenticity."""
from copy import deepcopy

from cawg_trqp_refimpl.experimental_consent_assurance import assess_consent
from test_experimental_consent_assurance import sample


def test_withdrawal_after_use_preserves_historical_claim_only():
    c = sample()
    c["evaluated_at"] = "2026-10-25T00:00:00Z"
    r = c["records"][0]
    r["withdrawn_effective_at"] = "2026-10-20T00:00:00Z"
    r["withdrawal_observed_at"] = "2026-10-21T00:00:00Z"
    result = assess_consent(c)
    assert result["consent_at_use_time"] == "claimed_in_scope"
    assert result["consent_current_state"] == "claimed_withdrawn"
    assert result["assured_consent"] == "indeterminate"


def test_withdrawal_before_use_never_claims_in_scope():
    c = sample()
    c["records"][0]["withdrawn_effective_at"] = "2026-10-05T00:00:00Z"
    c["records"][0]["withdrawal_observed_at"] = "2026-10-06T00:00:00Z"
    result = assess_consent(c)
    assert result["consent_at_use_time"] == "claimed_out_of_scope"
    assert result["reason"] == "claimed_withdrawal_before_use"
    assert result["consent_current_state"] == "claimed_withdrawn"


def test_unobserved_retrospective_withdrawal_cannot_claim_current_certainty():
    c = sample()
    c["records"][0]["withdrawn_effective_at"] = "2026-10-05T00:00:00Z"
    c["records"][0]["withdrawal_observed_at"] = "2026-10-20T00:00:00Z"
    result = assess_consent(c)
    assert result["consent_current_state"] == "indeterminate"
    assert result["reason"] == "withdrawal_not_observed_as_of_evaluation"
    assert result["assured_consent"] == "indeterminate"


def test_expiry_at_boundary_is_half_open():
    c = sample()
    c["used_at"] = "2026-10-31T00:00:00Z"
    result = assess_consent(c)
    assert result["consent_at_use_time"] == "claimed_out_of_scope"


def test_current_expiry_does_not_rewrite_claimed_use():
    c = sample()
    c["evaluated_at"] = "2026-11-02T00:00:00Z"
    result = assess_consent(c)
    assert result["consent_at_use_time"] == "claimed_in_scope"
    assert result["consent_current_state"] == "claimed_expired"


def test_repeated_replay_and_external_evidence_cannot_upgrade_assurance():
    c = sample()
    for value in ("a" * 64, "b" * 64):
        d = deepcopy(c)
        d["records"][0]["evidence_sha256"] = value
        x = assess_consent(d)
        assert x == assess_consent(deepcopy(d))
        assert x["consent_evidence_status"] == "unverified"
        assert x["assured_consent"] == "indeterminate"
