"""Assurance claims must never be elevated from synthetic fixture flags."""
import copy
import pytest
from test_experimental_delegated_creator import case
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate

def test_synthetic_authorization_never_becomes_assured():
    c = case()
    for credential in (False, True):
        c["chain"][0]["credential_verified"] = credential
        r = evaluate(c)
        assert r["historical_authority"] == "authorized"
        assert r["assured_authority"] == "indeterminate"
        assert r["assured_coverage"] == "unverified"
        assert r["assurance_reason"] == "independent_evidence_verification_unavailable"
        assert r["evidence_provenance"]["signing_time"] == "caller_supplied_untrusted"
        assert r["evidence_provenance"]["delegator_signature"] == "not_verified"

@pytest.mark.parametrize("mutation", [
    lambda c: c.update(signed_at=c["chain"][0]["not_before"]),
    lambda c: c.update(signed_at=c["chain"][0]["not_after"]),
    lambda c: c["chain"][0].update(revoked_at=c["signed_at"]),
    lambda c: c["chain"][0].update(credential_verified=True),
    lambda c: c["links"][0]["content"].update(consent=False),
])
def test_evidence_never_raises_assurance_on_boundary_or_tampering(mutation):
    c = case()
    mutation(c)
    r = evaluate(c)
    assert r["assured_authority"] == "indeterminate"
    assert r["assured_coverage"] == "unverified"

def test_replay_same_assurance_result():
    c=case()
    assert evaluate(c)==evaluate(copy.deepcopy(c))
