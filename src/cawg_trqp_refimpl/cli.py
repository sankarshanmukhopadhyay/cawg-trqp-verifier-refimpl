from __future__ import annotations

import argparse
import json
from pathlib import Path

from .audit import build_audit_bundle
from .fixture_loader import load_manifest_fixture
from .models import VerificationRequest
from .mock_service import MockTRQPService
from .snapshot import SnapshotStore
from .verifier import Verifier
from .gateway import TrustGateway


def main() -> None:
    parser = argparse.ArgumentParser(description="CAWG–TRQP reference verifier")
    parser.add_argument("request_json", nargs="?", help="Path to verification request JSON")
    parser.add_argument("--fixture", help="Path to CAWG/C2PA-style manifest fixture")
    parser.add_argument("--authority-id", default="did:web:media-registry.example")
    parser.add_argument("--profile", default="standard", choices=["edge", "standard", "high_assurance"])
    parser.add_argument("--policies", default="data/policies.json")
    parser.add_argument("--snapshot", default="data/snapshot.json")
    parser.add_argument("--trust-anchors", default="data/trust_anchors.json")
    parser.add_argument("--revocations", default="data/revocations.json")
    parser.add_argument("--use-gateway", action="store_true", help="Route live policy queries through trust gateway")
    parser.add_argument("--export-audit-bundle", help="Path to write audit bundle JSON")
    parser.add_argument("--exported-at", help="Deterministic timestamp override for audit bundle export")
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
    snapshot = None
    gateway = TrustGateway(service) if args.use_gateway and service is not None else None
    if args.profile == "edge":
        snapshot = SnapshotStore(root / args.snapshot, root / args.trust_anchors)
    verifier = Verifier(service=service, snapshot=snapshot, gateway=gateway)
    result = verifier.verify(request, profile=args.profile)
    print(json.dumps(result.to_dict(), indent=2))
    if args.export_audit_bundle:
        bundle = build_audit_bundle(
            request,
            result,
            profile=args.profile,
            use_gateway=args.use_gateway,
            exported_at=args.exported_at,
        )
        Path(args.export_audit_bundle).write_text(json.dumps(bundle.to_dict(), indent=2), encoding='utf-8')


if __name__ == "__main__":
    main()
