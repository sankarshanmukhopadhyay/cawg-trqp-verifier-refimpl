"""Session 4 cross-boundary adversarial checks; no claim of external trust."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

from cawg_trqp_refimpl.experimental_subject_evidence import assess_subject_evidence
from cawg_trqp_refimpl.experimental_consent_assurance import assess_consent
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate
from cawg_trqp_refimpl.external_c2pa_validation import validate_c2pa_asset
from test_experimental_consent_assurance import sample
from test_experimental_delegated_creator import case


def test_pseudonym_vouching_cannot_authorize_delegate_or_expose_identifier():
    subject = {
        "subject": "pairwise:private-performer-reference",
        "kind": "pseudonymous",
        "unique_claim": True,
        "vouching": [{"issuer": "guild:example", "kind": "professional",
                      "claimed_status": "verified", "scope": "performance"}],
    }
    outcome = assess_subject_evidence(subject)
    assert outcome["assured_subject_binding"] == "indeterminate"
    assert outcome["assured_authority"] == "indeterminate"
    assert outcome["vouching_sources"][0]["recognition"] == "not_checked"
    assert subject["subject"] not in json.dumps(outcome)
    delegated = case()
    delegated["actor"] = subject["subject"]
    result = evaluate(delegated)
    assert result["authority"] == "denied"
    assert result["assured_authority"] == "indeterminate"


def test_matching_registry_reference_and_digest_cannot_establish_consent():
    c = sample()
    c["records"][0]["evidence_ref"] = "https://registry.example.test/consent/opaque"
    c["records"][0]["evidence_sha256"] = "f" * 64
    matched = assess_consent(c)
    assert matched["consent_at_use_time"] == "claimed_in_scope"
    assert matched["consent_source_provenance"] == "caller_supplied_unverified"
    assert matched["assured_consent"] == "indeterminate"
    assert c["records"][0]["evidence_ref"] not in json.dumps(matched)
    cross_context = deepcopy(c)
    cross_context["subject_ref"] = "other-relationship-pseudonym"
    unmatched = assess_consent(cross_context)
    assert unmatched["consent_at_use_time"] == "claimed_out_of_scope"
    assert unmatched["assured_consent"] == "indeterminate"


def test_large_asset_digest_streams_without_read_bytes(tmp_path):
    payload = b"media" * (1024 * 1024)
    asset = tmp_path / "asset.jpg"
    asset.write_bytes(payload)
    report = {"active_manifest": "urn:fixture", "validation_status": []}
    completed = type("Completed", (), {
        "returncode": 0, "stdout": json.dumps(report).encode(), "stderr": b""
    })()
    with patch.object(Path, "read_bytes", side_effect=AssertionError("whole-file read")):
        with patch("cawg_trqp_refimpl.external_c2pa_validation.subprocess.run",
                   return_value=completed):
            result = validate_c2pa_asset(asset)
    assert result["asset_sha256"] == hashlib.sha256(payload).hexdigest()
    assert result["manifest_integrity"] == "validated_by_external_tool"
    assert result["signer_trust"] == "not_evaluated"
    assert result["delegated_authority"] == "not_evaluated"
    assert result["trusted_signing_time"] == "not_evaluated"
