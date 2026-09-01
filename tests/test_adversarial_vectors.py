import json
from pathlib import Path

from scripts.validate_adversarial_vectors import REQUIRED_CLASSES, validate


ROOT = Path(__file__).resolve().parents[1]


def test_adversarial_vector_contract_is_valid():
    assert validate() == []


def test_each_required_falsification_class_has_fail_safe_expectation():
    data = json.loads((ROOT / "conformance" / "adversarial-vectors.json").read_text())
    by_class = {vector["class"]: vector for vector in data["vectors"]}
    assert set(by_class) == REQUIRED_CLASSES
    for vector in by_class.values():
        assert vector["expected_trust_outcome"] in {"rejected", "deferred"}
        assert vector["expected_reason_code"]
        assert vector["proposition"]
        assert vector["mutation"]
        assert vector["risk_mapping"]
