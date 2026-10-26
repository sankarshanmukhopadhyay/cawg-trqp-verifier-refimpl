"""Portable five-world taskforce story corpus; normalized synthetic inputs only."""
import copy
import hashlib
import json
from pathlib import Path
import pytest
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate

DATA = json.loads((Path(__file__).resolve().parents[1] / "conformance" / "delegated-creator-five-world-scenarios.json").read_text())
def make_case(row):
    content = {"delegation_reference": row["name"], "agreement": "private off-manifest"}
    uri = "https://example.test/evidence/" + row["name"]
    digest = hashlib.sha256(json.dumps(content, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    chain = []
    for root, delegate in row["links"]:
        chain.append(dict(delegator=root, delegate=delegate, actions=[row["action"]],
                          resources=[row["resource"]], purposes=[row["purpose"]],
                          not_before=row["start"], not_after=row["end"],
                          redelegation=True, revoked_at=None, evidence_uri=uri,
                          credential_verified=False))
    return dict(id=row["name"], root_principal=row["root"], actor=row["actor"],
                action=row["action"], resource=row["resource"], purpose=row["purpose"],
                signed_at=row["sign"], evaluated_at=row["now"], chain=chain,
                links=[dict(uri=uri, sha256=digest, content=content)],
                generator=dict(id="taskforce-generator", reject_on_unverified=True))

@pytest.mark.parametrize("row", DATA["scenarios"], ids=lambda row: row["name"])
def test_story_positive_and_negative(row):
    c = make_case(row)
    result = evaluate(c)
    assert result["historical_authority"] == row["expect"]
    assert result["current_authority"] == row["current"]
    assert result["evidence_provenance"]["delegator_signature"] == "not_verified"
    assert result["evidence_provenance"]["signing_time"] == "caller_supplied_untrusted"
    assert result["coverage"] == "delegator-covered"  # simulated label only
    assert result["generator"] == "accepted"
    assert not any(key in result for key in ("agreement", "consent", "contract"))
    if row.get("creative_credit"):
        assert "creative_credit" not in result
    bad = copy.deepcopy(c)
    if row.get("negative"):
        bad["signed_at"] = row["negative"]
    elif row.get("negative_resource"):
        bad["resource"] = row["negative_resource"]
    elif row.get("negative_action"):
        bad["action"] = row["negative_action"]
    elif row.get("negative_redelegate"):
        bad["chain"][0]["redelegation"] = False
    assert evaluate(bad)["reason"] == row["negative_reason"]

def test_five_unique_worlds_and_reproducibility():
    assert len(DATA["scenarios"]) == 5
    assert len({r["world"] for r in DATA["scenarios"]}) == 5
    for row in DATA["scenarios"]:
        case = make_case(row)
        assert evaluate(case) == evaluate(copy.deepcopy(case))
