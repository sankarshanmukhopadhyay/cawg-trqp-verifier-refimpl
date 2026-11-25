"""Check complete question coverage and required Wave 1 minimum mappings."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_question_crosswalk_and_case_minimums():
    questions = json.loads((ROOT / "conformance/delegated-creator-session5-6-questions.json").read_text())
    assert [q["id"] for q in questions["questions"]] == [f"Q{i}" for i in range(1, 24)]
    assert all(q["assessment"] and q["disposition"] in
               {"local-partial", "upstream", "external", "external-upstream"}
               for q in questions["questions"])
    wave = json.loads((ROOT / "conformance/delegated-creator-wave1-coverage.json").read_text())
    for case in wave["cases"]:
        assert set(case["question_mapping"]) == {"Q5", "Q6", "Q9", "Q10"}
        assert all(case["question_mapping"].values())
        assert case["candidate_assertions"]
        assert case["specification_issue"]
        assert case["policy_review"]


def test_story_and_controls_traceability():
    wave = json.loads((ROOT / "conformance/delegated-creator-wave1-coverage.json").read_text())
    for case in wave["cases"]:
        assert set(case["story"]) == {
            "vision", "actors", "scope", "preconditions", "success", "extensions",
            "frequency", "special_requirements",
        }
        assert all(case["story"].values())
        assert all((ROOT / p).is_file() for p in case["verifier_tests"])
    controls = json.loads((ROOT / "conformance/delegated-creator-session5-6-controls.json").read_text())
    assert len(controls["controls"]) == 10
    assert len({c["id"] for c in controls["controls"]}) == 10
    for control in controls["controls"]:
        assert control["condition"] and control["disposition"] and control["inventory"]
        assert (ROOT / control["test"]).is_file()
        assert all(q in {f"Q{i}" for i in range(1, 24)} for q in control["questions"])
