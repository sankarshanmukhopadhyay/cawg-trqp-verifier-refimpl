#!/usr/bin/env python3
"""Emit deterministic Wave 1 results from the real local consumer path."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

from cawg_trqp_refimpl.experimental_taskforce_assessment import assess_operation
from taskforce_wave1_fixtures import CASES, PUBLIC, ROOT, inputs


def report():
    schema = json.loads((ROOT / "schemas/experimental-taskforce-operation.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    results = []
    for case in CASES:
        request, envelope, records, subject = inputs(case)
        actual = assess_operation(request, envelope, PUBLIC, consent_records=records,
                                  subject_evidence=subject)
        expected = {
            "request_status": "valid", "statement_integrity": "verified",
            "delegation_at_use": "signed_terms_in_scope",
            "delegation_current": "signed_terms_in_scope",
            "consent_at_use": "claimed_in_scope" if records else "indeterminate",
            "assured_authority": "indeterminate", "assured_consent": "indeterminate",
        }
        validator.validate(actual)
        # Also run a negative case through the same public consumer path.
        negative = assess_operation(dict(request, actor="different-actor"),
                                    envelope, PUBLIC, consent_records=records,
                                    subject_evidence=subject)
        validator.validate(negative)
        matches = (all(actual[k] == v for k, v in expected.items())
                   and negative["delegation_at_use"] == "signed_terms_out_of_scope"
                   and negative["assured_authority"] == "indeterminate")
        results.append({"scenario": case["id"], "expected": expected,
                        "actual": actual, "wrong_actor": negative, "matches": matches})
    return {"format_version": "0.1", "source": "public deterministic fixture keys",
            "local_cryptographic_integrity": True,
            "independent_interoperability": False,
            "independent_consent_verification": False,
            "all_match": len(results) == 6 and all(x["matches"] for x in results),
            "results": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = report()
    payload = json.dumps(data, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0 if data["all_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
