#!/usr/bin/env python3
"""Emit an independently reproducible, non-authoritative synthetic assessment."""
from __future__ import annotations

import json
from pathlib import Path

from cawg_trqp_refimpl.experimental_consent_assurance import assess_consent
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate
from cawg_trqp_refimpl.taskforce_scenarios import make_case, read_scenarios

ROOT = Path(__file__).resolve().parents[1]


def report():
    corpus = json.loads((ROOT / "conformance/delegated-creator-consent-scenarios.json").read_text())
    worlds = {row["name"]: row for row in read_scenarios()}
    results = []
    for row in corpus["scenarios"]:
        delegation = evaluate(make_case(worlds[row["delegation_world"]]))
        consent = assess_consent(row["consent_case"])
        results.append({"scenario": row["name"], "delegation": {
            "historical_authority": delegation["historical_authority"],
            "current_authority": delegation["current_authority"],
            "assured_authority": delegation["assured_authority"],
            "signing_time_provenance": delegation["evidence_provenance"]["signing_time"]
        }, "consent": consent})
    return {"format_version": "0.1", "source": "repository-local synthetic fixtures",
            "independent_consent_verification": False,
            "independent_interoperability": False,
            "all_match": all(x["delegation"]["historical_authority"] == "authorized" and
                             x["consent"]["consent_at_use_time"] == "claimed_in_scope" and
                             x["consent"]["assured_consent"] == "indeterminate"
                             for x in results), "results": results}


if __name__ == "__main__":
    print(json.dumps(report(), sort_keys=True, indent=2))
