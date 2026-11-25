"""Authenticated local source claims; no assertion of independent governance."""
import hashlib
import json
from datetime import datetime, timezone

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from cawg_trqp_refimpl.experimental_source_evidence import (
    PROFILE, PinnedEvidenceSource,
)
from cawg_trqp_refimpl.experimental_taskforce_assessment import assess_operation
from cawg_trqp_refimpl.experimental_two_party_delegation import signing_bytes
from cawg_trqp_refimpl.feed_descriptor import sign_feed_descriptor
from cawg_trqp_refimpl.jsoncanon import canonical_json_bytes
from test_taskforce_wave1_assessment import CASES, inputs, PUBLIC, CONTEXT

SOURCE = Ed25519PrivateKey.from_private_bytes(b"\x03" * 32)
SOURCE_PEM = SOURCE.public_key().public_bytes(
    serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
).decode()
NOW = datetime(2026, 11, 25, tzinfo=timezone.utc)


def policy(kind):
    return PinnedEvidenceSource(kind, "fixture:private-registry", "source-key",
                                SOURCE_PEM, 3600)


def package(kind, claim, state="active", *, issued="2026-11-24T23:30:00Z",
            expiry="2026-11-25T01:00:00Z", source_id="fixture:private-registry",
            key_id="source-key", private=SOURCE, scope=None):
    body = canonical_json_bytes({
        "profile": PROFILE, "kind": kind, "claim": claim, "state": state,
    })
    descriptor = {
        "descriptor_type": "cawg-trqp-feed-descriptor", "descriptor_version": "1.0.0",
        "descriptor_id": "fixture:private-descriptor", "issued_at": issued,
        "valid_until": expiry,
        "authority": {"authority_id": source_id, "key_id": key_id,
                      "scope": ["experimental-taskforce:" + kind] if scope is None else scope},
        "feed": {"feed_type": "revocation_feed" if kind == "delegation-status" else "policy_feed",
                 "source": "https://example.test/private/source",
                 "digest_alg": "sha-256", "digest_sha256": hashlib.sha256(body).hexdigest()},
        "freshness": {"max_age_seconds": 7200, "enforcement": "fail"},
        "route": {"channel": "offline", "attested": False},
    }
    return canonical_json_bytes(sign_feed_descriptor(descriptor, private, key_id=key_id)), body


def evidence_inputs():
    req, env, records, subject = inputs(CASES[0])
    hashes = {role: hashlib.sha256(key).hexdigest() for role, key in PUBLIC.items()}
    terms = {"statement_sha256": hashlib.sha256(signing_bytes(
        env["statement"], CONTEXT, "delegator", "delegator")).hexdigest(),
        "delegator_key_sha256": hashes["delegator"], "delegate_key_sha256": hashes["delegate"]}
    claims = {
        "delegator_binding": ("subject-key-binding",
                              {"subject_ref": req["principal"], "key_sha256": hashes["delegator"]}, "active"),
        "delegate_binding": ("subject-key-binding",
                             {"subject_ref": req["actor"], "key_sha256": hashes["delegate"]}, "active"),
        "authority_to_delegate": ("authority-to-delegate", terms, "active"),
        "delegation_status": ("delegation-status", terms, "active"),
        "consent_record": ("consent-record", {
            "subject_ref": req["consent_subject"],
            "record_sha256": hashlib.sha256(canonical_json_bytes(records[0])).hexdigest(),
        }, "attested"),
    }
    packages = {name: package(kind, claim, state) for name, (kind, claim, state) in claims.items()}
    policies = {name: policy(kind) for name, (kind, _, _) in claims.items()}
    return req, env, records, subject, claims, packages, policies


def assess(data, *, now=NOW):
    req, env, records, subject, _, packages, policies = data
    return assess_operation(req, env, PUBLIC, consent_records=records, subject_evidence=subject,
                            source_packages=packages, source_policies=policies,
                            source_observed_at=now)


def test_all_five_source_claims_are_authenticated_not_assured_authority():
    report = assess(evidence_inputs())
    for name, evidence in report["source_evidence"].items():
        assert evidence["status"] == "authenticated_source_claim", name
    assert report["source_evidence"]["consent_record"]["state"] == "attested"
    assert report["assured_authority"] == report["assured_consent"] == "indeterminate"
    assert report["trusted_time"] == report["c2pa_binding"] == "not_checked"
    text = json.dumps(report)
    for private in ("fixture:private", "https://example.test", "opaque:", "source-key"):
        assert private not in text


@pytest.mark.parametrize("mutation,expected", [
    ("wrong-key", "invalid"), ("wrong-source", "unrecognized"),
    ("wrong-scope", "unrecognized"), ("stale", "stale"),
    ("future", "stale"), ("expired", "stale"), ("wrong-claim", "mismatch"),
    ("tampered-body", "invalid"), ("duplicate-json", "invalid"),
    ("unknown-policy", "unrecognized"),
])
def test_source_boundaries(mutation, expected):
    data = evidence_inputs()
    kind, claim, state = data[4]["delegate_binding"]
    options = {}
    if mutation == "wrong-key":
        options["private"] = Ed25519PrivateKey.from_private_bytes(b"\x04" * 32)
    elif mutation == "wrong-source":
        options["source_id"] = "fixture:unrecognized"
    elif mutation == "wrong-scope":
        options["scope"] = ["unrelated"]
    elif mutation == "stale":
        options["issued"] = "2026-11-24T22:59:59Z"
    elif mutation == "future":
        options["issued"] = "2026-11-25T00:00:01Z"
    elif mutation == "expired":
        options["expiry"] = "2026-11-25T00:00:00Z"
    elif mutation == "wrong-claim":
        claim = dict(claim, subject_ref="other-subject")
    elif mutation == "unknown-policy":
        del data[6]["delegate_binding"]
    signed = package(kind, claim, state, **options)
    if mutation == "tampered-body":
        signed = signed[0], signed[1].replace(b"active", b"revoked")
    elif mutation == "duplicate-json":
        signed = signed[0], signed[1].replace(b'"state":"active"', b'"state":"active","state":"active"')
    data[5]["delegate_binding"] = signed
    report = assess(data)
    assert report["source_evidence"]["delegate_binding"]["status"] == expected
    assert report["assured_authority"] == "indeterminate"


def test_status_and_consent_stay_separate_even_with_failed_delegation():
    data = evidence_inputs()
    kind, claim, _ = data[4]["delegation_status"]
    data[5]["delegation_status"] = package(kind, claim, "revoked")
    report = assess(data)
    assert report["source_evidence"]["delegation_status"]["state"] == "revoked"
    assert report["source_evidence"]["consent_record"]["state"] == "attested"
    assert report["assured_authority"] == "indeterminate"
    data[1]["signatures"].pop("delegate")
    report = assess(data)
    assert report["statement_integrity"] == "invalid"
    assert report["source_evidence"]["authority_to_delegate"]["status"] == "indeterminate"
    assert report["source_evidence"]["consent_record"]["status"] == "authenticated_source_claim"


def test_consent_receipt_cannot_replay_against_changed_record_or_clock():
    data = evidence_inputs()
    data[2][0]["withdrawn_effective_at"] = "2026-11-24T00:00:00Z"
    data[2][0]["withdrawal_observed_at"] = "2026-11-24T12:00:00Z"
    report = assess(data)
    assert report["consent_current"] == "claimed_withdrawn"
    assert report["source_evidence"]["consent_record"]["status"] == "mismatch"
    report = assess(data, now=None)
    assert report["source_evidence"]["consent_record"]["status"] == "indeterminate"
    assert report["assured_consent"] == "indeterminate"
