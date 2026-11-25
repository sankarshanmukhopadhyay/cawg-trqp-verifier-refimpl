"""Public, deterministic non-production fixtures for the Wave 1 demonstration."""
from __future__ import annotations

import base64
import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from cawg_trqp_refimpl.experimental_two_party_delegation import signing_bytes

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "conformance/delegated-creator-wave1-coverage.json").read_text(encoding="utf-8"))
CASES = CATALOG["cases"]
KEYS = {role: Ed25519PrivateKey.from_private_bytes(bytes([i]) * 32)
        for i, role in enumerate(("delegator", "delegate"), 1)}
PUBLIC = {role: key.public_key().public_bytes(
    serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    for role, key in KEYS.items()}
CONTEXT = "a" * 64


def inputs(case):
    request = {k: case[k] for k in ("principal", "actor", "action", "resource",
                                    "purpose", "consent_subject")}
    request.update(used_at="2026-11-23T00:00:00Z",
                   evaluated_at="2026-11-25T00:00:00Z", context_sha256=CONTEXT)
    statement = {"delegator": case["principal"], "delegate": case["actor"],
                 "actions": [case["action"]], "resources": [case["resource"]],
                 "purposes": [case["purpose"]],
                 "not_before": "2026-11-20T00:00:00Z",
                 "not_after": "2026-12-04T00:00:00Z"}
    envelope = {"statement": statement, "context_sha256": CONTEXT,
                "signatures": {role: {
                    "key_id": role, "signature_b64": base64.b64encode(key.sign(
                        signing_bytes(statement, CONTEXT, role, role))).decode()
                } for role, key in KEYS.items()}}
    records = []
    if case["consent_subject"]:
        records.append({
            "record_id": "private-record", "subject_ref": case["consent_subject"],
            "actions": [case["action"]], "resources": [case["resource"]],
            "purposes": [case["purpose"]], "valid_from": "2026-11-20T00:00:00Z",
            "valid_until": "2026-12-04T00:00:00Z", "withdrawn_effective_at": None,
            "withdrawal_observed_at": None,
            "evidence_ref": "https://example.test/private/secret",
            "evidence_sha256": "b" * 64,
        })
    subject = {"subject": case["actor"], "kind": "pseudonymous",
               "unique_claim": True, "vouching": [{"issuer": "private-registry",
                    "kind": "professional", "claimed_status": "verified", "scope": "creator"}]}
    return request, envelope, records, subject

