import math

import pytest

from cawg_trqp_refimpl.models import VerificationRequest


def request(**overrides):
    values = {
        "asset_id": "asset:test",
        "integrity_ok": True,
        "entity_id": "did:web:publisher.example",
        "authority_id": "did:web:media-registry.example",
        "issuer_id": None,
        "action": "publish",
        "resource": "cawg:news-content",
        "context": {},
        "process_evidence": None,
    }
    values.update(overrides)
    return VerificationRequest(**values)


@pytest.mark.parametrize("confidence", ["abc", [], {}, -0.01, 1.01, math.nan, math.inf, -math.inf, True])
def test_rejects_invalid_process_confidence(confidence):
    with pytest.raises(ValueError, match="confidence"):
        request(process_evidence={"confidence": confidence})


def test_accepts_process_confidence_boundaries():
    assert request(process_evidence={"confidence": 0}).process_evidence["confidence"] == 0
    assert request(process_evidence={"confidence": 1.0}).process_evidence["confidence"] == 1.0


@pytest.mark.parametrize("field", ["process_type", "evidence_ref", "evidence_format", "appraisal", "reference"])
def test_rejects_non_string_process_evidence_fields(field):
    with pytest.raises(ValueError, match=field):
        request(process_evidence={field: []})


def test_rejects_non_boolean_verified():
    with pytest.raises(ValueError, match="verified"):
        request(process_evidence={"verified": "yes"})


def test_rejects_non_object_context():
    with pytest.raises(ValueError, match="context"):
        request(context=[])


def test_rejects_non_object_process_evidence():
    with pytest.raises(ValueError, match="process_evidence"):
        request(process_evidence=[])
