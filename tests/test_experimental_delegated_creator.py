"""Deterministic experimental vectors. No upstream CAWG conformance is asserted."""
import copy
import hashlib
import json
from datetime import datetime, timezone
import pytest
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate, InvalidCase

def case():
    evidence = {"agreement": "creator delegates scoped publication", "consent": True}
    uri = "https://example.test/consent/123"
    digest = hashlib.sha256(json.dumps(evidence, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    edge = {
        "delegator": "creator", "delegate": "studio", "actions": ["create", "publish"],
        "resources": ["asset:1"], "purposes": ["editorial"], "not_before": "2026-10-01T00:00:00Z",
        "not_after": "2026-10-31T00:00:00Z", "redelegation": True, "revoked_at": None,
        "evidence_uri": uri, "credential_verified": False
    }
    return {
        "id": "publisher-direct", "root_principal": "creator", "actor": "studio",
        "action": "publish", "resource": "asset:1", "purpose": "editorial",
        "signed_at": "2026-10-23T10:00:00Z", "evaluated_at": "2026-10-23T10:00:01Z",
        "links": [{"uri": uri, "sha256": digest, "content": evidence}],
        "chain": [edge], "generator": {"id": "claim-gen", "reject_on_unverified": True}
    }

@pytest.mark.parametrize("mutation,reason,authority", [
    (lambda c: c["chain"].clear(), "no_delegation", "indeterminate"),
    (lambda c: c.update(action="transform"), "requested_action_out_of_scope", "denied"),
    (lambda c: c["chain"][0].update(not_after="2026-10-22T00:00:00Z"), "not_valid_at_signing", "denied"),
    (lambda c: c["chain"][0].update(revoked_at="2026-10-23T09:00:00Z"), "revoked_at_signing", "denied"),
    (lambda c: c["chain"][0].update(revoked_at="2026-10-23T10:00:00.5Z"), "revoked_at_evaluation", "denied"),
    (lambda c: c["links"][0]["content"].update(consent=False), "linked_evidence_integrity", "indeterminate"),
    (lambda c: c.update(actor="intruder"), "actor_not_delegate", "denied"),
    (lambda c: c["chain"][0].update(evidence_uri="https://example.test/unknown"), "delegation_evidence_unavailable", "indeterminate"),
    (lambda c: c["chain"][0].update(not_after="2027-04-22T00:00:00Z"), "delegation_duration_exceeded", "denied"),
])
def test_vectors(mutation, reason, authority):
    c = case()
    mutation(c)
    result = evaluate(c)
    assert (result["reason"], result["authority"], result["generator"]) == (reason, authority, "rejected")

def test_positive_provenance_separate_from_authorization():
    r = evaluate(case())
    assert r["coverage"] == "delegator-covered"
    assert r["authority"] == "authorized"
    assert r["generator"] == "accepted"
    assert r["evidence_sha256"]

def test_credential_classification_is_not_independent_credential_verification():
    c = case()
    c["chain"][0]["credential_verified"] = True
    assert evaluate(c)["coverage"] == "credential-backed"

def test_agentic_attenuation_and_depth():
    c = case()
    c["actor"] = "agent"
    second = copy.deepcopy(c["chain"][0])
    second.update(delegator="studio", delegate="agent", actions=["publish"], redelegation=False)
    c["chain"].append(second)
    assert evaluate(c)["authority"] == "authorized"
    second["actions"] = ["publish", "transform"]
    assert evaluate(c)["reason"] == "scope_or_duration_escalation"
    second["actions"] = ["publish"]
    c["chain"][0]["redelegation"] = False
    assert evaluate(c)["reason"] == "redelegation_forbidden"
    c["chain"][0]["redelegation"] = True
    for i in range(2):
        extra = copy.deepcopy(second)
        extra.update(delegator=["agent", "agent2"][i], delegate=["agent2", "agent3"][i])
        c["chain"].append(extra)
    assert evaluate(c)["reason"] == "chain_depth_exceeded"

def test_cycle_and_chain_break():
    c = case()
    c["actor"] = "creator"
    c["chain"][0]["delegate"] = "creator"
    assert evaluate(c)["reason"] == "chain_cycle"
    c["chain"][0]["delegator"] = "someone"
    assert evaluate(c)["reason"] == "chain_disconnected"

@pytest.mark.parametrize("field,value", [("signed_at","bad"), ("evaluated_at","2026-10-23T10:00:01"),
                                         ("action","forbidden"), ("links","wrong"), ("chain",None)])
def test_invalid_inputs(field,value):
    c=case()
    c[field]=value
    with pytest.raises(InvalidCase):
        evaluate(c)

def test_indeterminate_generator_policy_does_not_authorize():
    c = case()
    c["chain"].clear()
    c["generator"]["reject_on_unverified"] = False
    r = evaluate(c)
    assert r["generator"] == "accepted"
    assert r["authority"] == "indeterminate"

def test_replay_is_deterministic():
    c=case()
    assert evaluate(c)==evaluate(copy.deepcopy(c))
