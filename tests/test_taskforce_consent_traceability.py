"""Validate the public cross-taskforce evidence map and all local references."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_consent_traceability_has_bounded_non_normative_evidence():
    path = ROOT / "conformance/delegated-creator-consent-traceability.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["schema_version"] == "0.1"
    assert "informative" in data["status"]
    assert len(data["propositions"]) == 8
    identifiers = [row["id"] for row in data["propositions"]]
    assert len(set(identifiers)) == 8
    assert all(x.startswith("DC-CONSENT-") for x in identifiers)
    for row in data["propositions"]:
        assert row["disposition"] in {
            "locally-tested", "external-evidence-required",
            "upstream-decision-required", "out-of-scope",
        }
        assert row["evidence"]
        for ref in row["evidence"]:
            target = (ROOT / ref).resolve()
            assert target.is_relative_to(ROOT)
            assert target.is_file(), ref
