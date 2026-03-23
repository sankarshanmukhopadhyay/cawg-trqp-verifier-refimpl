from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path

from cryptography.hazmat.primitives import serialization

from cawg_trqp_refimpl.snapshot import SnapshotStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Sign a CAWG-TRQP offline snapshot with Ed25519")
    parser.add_argument("snapshot", help="Path to unsigned snapshot JSON")
    parser.add_argument("private_key", help="Path to Ed25519 private key PEM")
    parser.add_argument("--key-id", required=True, help="Trust-anchor key identifier")
    parser.add_argument("--output", help="Output path. Defaults to in-place write")
    args = parser.parse_args()

    snapshot_path = Path(args.snapshot)
    data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    data.pop("signature", None)

    private_key = serialization.load_pem_private_key(Path(args.private_key).read_bytes(), password=None)
    payload = SnapshotStore._canonical_payload(data)
    signature = private_key.sign(payload)
    data["signature"] = {
        "algorithm": "Ed25519",
        "key_id": args.key_id,
        "value": base64.b64encode(signature).decode("ascii"),
    }

    output_path = Path(args.output) if args.output else snapshot_path
    output_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
