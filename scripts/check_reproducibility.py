from __future__ import annotations

import argparse
import json
from pathlib import Path

from cawg_trqp_refimpl.audit import build_audit_bundle
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.validation import load_json
from cawg_trqp_refimpl.verifier import Verifier



def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild and compare a deterministic CAWG-TRQP audit bundle fixture")
    parser.add_argument("expected_bundle", help="Path to expected audit bundle fixture JSON")
    parser.add_argument("--request", default="examples/verification_request.json")
    parser.add_argument("--policies", default="data/policies.json")
    parser.add_argument("--revocations", default="data/revocations.json")
    parser.add_argument("--exported-at", default="2026-03-31T00:00:00Z")
    args = parser.parse_args()

    request = VerificationRequest(**load_json(args.request))
    verifier = Verifier(service=MockTRQPService(args.policies, args.revocations))
    result = verifier.verify(request, profile="standard")
    actual = build_audit_bundle(
        request,
        result,
        profile="standard",
        exported_at=args.exported_at,
        policy_path=args.policies,
        revocation_path=args.revocations,
    ).to_dict()
    expected = load_json(args.expected_bundle)

    if actual != expected:
        print(json.dumps({"matches": False, "expected": expected, "actual": actual}, indent=2))
        raise SystemExit(1)

    print(json.dumps({"matches": True, "bundle_id": actual.get("bundle_id")}, indent=2))


if __name__ == "__main__":
    main()
