#!/usr/bin/env python3
"""Emit portable Taskforce scenario decisions; exits nonzero if fixture expectations differ."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate
from cawg_trqp_refimpl.taskforce_scenarios import read_scenarios, make_case

def run():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, help="Optional JSON output file; default stdout")
    args = p.parse_args()
    entries=[]
    failed=False
    for row in read_scenarios():
        decision=evaluate(make_case(row))
        expected={"historical_authority":row["expect"],"current_authority":row["current"]}
        matched=all(decision.get(k)==v for k,v in expected.items())
        failed = failed or not matched
        entries.append({"scenario":row["name"],"world":row["world"],
                        "expected":expected,"actual":decision,"matches":matched})
    report={"format_version":"1","source":"experimental; synthetic fixtures",
            "independent_crypto_verification":False,
            "independent_interoperability":False,
            "all_match":not failed,"results":entries}
    payload=json.dumps(report,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")
    return 1 if failed else 0

if __name__=="__main__":
    raise SystemExit(run())
