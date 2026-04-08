from __future__ import annotations

import argparse
import json
from pathlib import Path

from cawg_trqp_refimpl.attestation import sign_audit_bundle_from_path
from cawg_trqp_refimpl.validation import load_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Sign a CAWG-TRQP audit bundle with Ed25519")
    parser.add_argument("bundle_json", help="Path to unsigned audit bundle JSON")
    parser.add_argument("private_key", help="Path to Ed25519 private key PEM")
    parser.add_argument("--key-id", required=True, help="Trust-anchor key identifier")
    parser.add_argument("--output", help="Output path. Defaults to in-place write")
    args = parser.parse_args()

    bundle = load_json(args.bundle_json)
    signed_bundle = sign_audit_bundle_from_path(bundle, args.private_key, key_id=args.key_id)
    output_path = Path(args.output) if args.output else Path(args.bundle_json)
    output_path.write_text(json.dumps(signed_bundle, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
