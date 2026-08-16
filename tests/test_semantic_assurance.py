from copy import deepcopy
from pathlib import Path

from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.profile import load_profile
from cawg_trqp_refimpl.verifier import Verifier


def _verifier():
    return Verifier(service=MockTRQPService(Path("data/policies.json"), Path("data/revocations.json")))


def _base_profile():
    return load_profile("standard").to_dict()


def test_required_assertion_missing_fails_before_authority_lookup():
    request = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_c2pa.json"), "did:web:media-registry.example")
    profile = _base_profile()
    profile["id"] = "required-identity"
    profile["controls"]["assertions"].update({
        "required_labels": ["cawg.identity"],
        "missing_required": "fail",
    })
    result = _verifier().verify(request, profile=profile)
    assert result.trust_outcome == "rejected"
    assert result.verification_mode == "semantic_guardrail"
    assert result.assertion_evaluation["missing"] == ["cawg.identity"]
    assert result.propositions["actor_authorization"]["status"] == "not_evaluated"


def test_missing_required_assertion_warns_as_degraded_not_trusted():
    request = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_c2pa.json"), "did:web:media-registry.example")
    profile = _base_profile()
    profile["id"] = "warning-identity"
    profile["controls"]["assertions"].update({
        "required_labels": ["cawg.identity"],
        "missing_required": "warn",
    })
    result = _verifier().verify(request, profile=profile)
    assert result.actor_authorization == "authorized"
    assert result.trust_outcome == "degraded"
    assert result.assertion_evaluation["status"] == "warning"


def test_conflicting_assertions_fail_under_explicit_policy():
    request = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_c2pa.json"), "did:web:media-registry.example")
    request.context["_manifest_assertions"] = [
        {"label": "cawg.consent", "data": {"training": "prohibited"}},
        {"label": "cawg.training-mining", "data": {"training": "allowed"}},
    ]
    profile = _base_profile()
    profile["id"] = "conflict-fail"
    profile["controls"]["conflicts"] = {
        "enforcement": "fail",
        "rules": [{
            "id": "training-use",
            "labels": ["cawg.consent", "cawg.training-mining"],
            "claim_path": "training",
            "strategy": "unresolved",
        }],
    }
    result = _verifier().verify(request, profile=profile)
    assert result.trust_outcome == "rejected"
    assert result.conflict_evaluation["status"] == "conflicted"
    assert result.conflict_evaluation["findings"][0]["status"] == "conflicted"


def test_precedence_rule_records_resolution_without_inventing_global_semantics():
    request = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_c2pa.json"), "did:web:media-registry.example")
    request.context["_manifest_assertions"] = [
        {"label": "cawg.consent", "data": {"training": "prohibited"}},
        {"label": "cawg.training-mining", "data": {"training": "allowed"}},
    ]
    profile = _base_profile()
    profile["id"] = "conflict-precedence"
    profile["controls"]["conflicts"] = {
        "enforcement": "fail",
        "rules": [{
            "id": "training-use",
            "labels": ["cawg.consent", "cawg.training-mining"],
            "claim_path": "training",
            "strategy": "precedence",
            "precedence": ["cawg.consent", "cawg.training-mining"],
        }],
    }
    result = _verifier().verify(request, profile=profile)
    assert result.trust_outcome == "trusted"
    finding = result.conflict_evaluation["findings"][0]
    assert finding["status"] == "resolved"
    assert finding["selected"] == {"label": "cawg.consent", "value": "prohibited"}


def test_risk_traceability_map_is_machine_readable_and_links_raHP_findings():
    import yaml
    data = yaml.safe_load(Path("conformance/risk-to-test-map.yaml").read_text())
    trace = data["external_assurance_traceability"]
    assert trace["reference_work"]["runtime_dependency"] is False
    assert {item["rahp_risk"] for item in trace["mappings"]} >= {"CRK-04", "CRK-12", "CRK-23", "CRK-28"}


def test_high_assurance_rejects_semantic_degradation_and_exposes_mandatory_gap():
    request = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_c2pa.json"), "did:web:media-registry.example")
    profile = _base_profile()
    profile["id"] = "high-assurance-semantic"
    profile["controls"]["decision"]["degraded_disposition"] = "reject"
    profile["controls"]["assertions"].update({
        "required_labels": ["cawg.identity"],
        "missing_required": "warn",
    })
    result = _verifier().verify(request, profile=profile)
    assert result.actor_authorization == "authorized"
    assert result.trust_outcome == "rejected"
    assert result.propositions["assertion_expectation"]["missing_mandatory"] == ["cawg.identity"]
    assert "Degraded semantic evidence disposition: reject" in result.explanations


def test_precedence_evidence_identifies_policy_source_classification_and_profile():
    request = load_manifest_fixture(Path("examples/fixtures/cawg_manifest_c2pa.json"), "did:web:media-registry.example")
    request.context["_manifest_assertions"] = [
        {"label": "cawg.consent", "data": {"training": "prohibited"}},
        {"label": "cawg.training-mining", "data": {"training": "allowed"}},
    ]
    profile = _base_profile()
    profile["id"] = "precedence-evidence"
    profile["controls"]["conflicts"] = {
        "enforcement": "fail",
        "rules": [{
            "id": "training-use",
            "labels": ["cawg.consent", "cawg.training-mining"],
            "claim_path": "training",
            "strategy": "precedence",
            "precedence": ["cawg.consent", "cawg.training-mining"],
            "policy_source": "relying-party:training-policy:v1",
            "source_classification": "illustrative-policy",
        }],
    }
    result = _verifier().verify(request, profile=profile)
    finding = result.conflict_evaluation["findings"][0]
    assert finding["precedence_applied"] == ["cawg.consent", "cawg.training-mining"]
    assert finding["policy_source"] == "relying-party:training-policy:v1"
    assert finding["source_classification"] == "illustrative-policy"
    assert result.conflict_evaluation["policy_profile"] == "precedence-evidence"
