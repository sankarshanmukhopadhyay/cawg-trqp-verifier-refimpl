from __future__ import annotations
import argparse
import json
from pathlib import Path
from .fixture_loader import load_manifest_fixture
from .models import VerificationRequest
from .mock_service import MockTRQPService
from .snapshot import SnapshotStore
from .verifier import Verifier


def main() -> None:
    parser = argparse.ArgumentParser(description="CAWG–TRQP reference verifier")
    parser.add_argument("request_json", nargs="?", help="Path to verification request JSON")
    parser.add_argument("--fixture", help="Path to CAWG/C2PA-style manifest fixture")
    parser.add_argument("--authority-id", default="did:web:media-registry.example")
    parser.add_argument("--profile", default="standard", choices=["edge", "standard", "high_assurance"])
    parser.add_argument("--policies", default="data/policies.json")
    parser.add_argument("--snapshot", default="data/snapshot.json")
    parser.add_argument("--revocations", default="data/revocations.json")
    args = parser.parse_args()

    root = Path.cwd()
    if args.fixture:
        request = load_manifest_fixture(root / args.fixture, authority_id=args.authority_id)
    elif args.request_json:
        request_data = json.loads((root / args.request_json).read_text(encoding="utf-8"))
        request = VerificationRequest(**request_data)
    else:
        raise SystemExit("Provide either request_json or --fixture")

    service = None if args.profile == "edge" else MockTRQPService(root / args.policies, root / args.revocations)
    snapshot = SnapshotStore(root / args.snapshot) if args.profile == "edge" else None
    verifier = Verifier(service=service, snapshot=snapshot)
    result = verifier.verify(request, profile=args.profile)
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
