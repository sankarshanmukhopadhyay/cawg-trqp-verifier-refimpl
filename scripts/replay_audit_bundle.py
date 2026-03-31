from __future__ import annotations

import argparse
import json

from cawg_trqp_refimpl.replay import replay_audit_bundle
from cawg_trqp_refimpl.validation import load_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay a CAWG-TRQP audit bundle against current policy data")
    parser.add_argument("bundle_json", help="Path to audit bundle JSON")
    parser.add_argument("--policies", default="data/policies.json")
    parser.add_argument("--revocations", default="data/revocations.json")
    args = parser.parse_args()

    bundle = load_json(args.bundle_json)
    report = replay_audit_bundle(bundle, policy_path=args.policies, revocation_path=args.revocations)
    print(json.dumps({
        "matches": report.matches,
        "differences": report.differences,
        "replayed_result": report.replayed_result,
    }, indent=2))
    if not report.matches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
