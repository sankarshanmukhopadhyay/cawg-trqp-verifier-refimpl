import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/property-listing-ai-images"


def load(name):
    return json.loads((EXAMPLE / name).read_text(encoding="utf-8"))


def test_property_listing_example_is_complete_and_machine_readable():
    for name in ["listing-submission.json", "listing-policy.json", "decision-receipt.json"]:
        assert (EXAMPLE / name).is_file()
        load(name)


def test_property_listing_decision_preserves_authority_and_disclosure():
    submission = load("listing-submission.json")
    policy = load("listing-policy.json")
    receipt = load("decision-receipt.json")

    assert submission["actor"]["role"] == "licensed_realtor"
    assert submission["context"]["seller_mandate_id"]
    assert submission["provenance"]["manifest_valid"] is True
    assert any(t["type"] == "generative_staging" and t["declared"] for t in submission["provenance"]["transformations"])
    assert "generative_staging" in policy["rules"]["disclosure_required_for"]
    assert policy["rules"]["failure_behavior"]["undeclared_ai_edit"] == "reject"
    assert receipt["decision"]["result"] == "conditionally_trusted"
    assert receipt["decision"]["required_disclosure"]
    assert receipt["evidence"]["appeal_supported"] is True


def test_property_listing_docs_state_the_assurance_boundary():
    doc = (ROOT / "docs/workflows/property-listing-ai-image-verification.md").read_text(encoding="utf-8")
    for marker in [
        "does not treat content credentials as proof that a property matches the image",
        "Authority binding",
        "Revocation",
        "Evidence and redress",
        "Undeclared AI edit",
    ]:
        assert marker in doc
