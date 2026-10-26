"""Portable synthetic scenario adapter for the five Taskforce creative worlds."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "conformance" / "delegated-creator-five-world-scenarios.json"

def read_scenarios(path: Path = CATALOG):
    catalog = json.loads(path.read_text(encoding="utf-8"))
    if catalog.get("schema_version") != "0.1" or len(catalog.get("scenarios", [])) != 5:
        raise ValueError("scenario_catalog_invalid")
    return catalog["scenarios"]

def make_case(row):
    # Mock inputs deliberately remain private to this local synthetic harness.
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
