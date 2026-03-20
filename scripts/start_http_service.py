#!/usr/bin/env python3
"""Start the HTTP TRQP service.

This script launches the Flask-based HTTP TRQP service, exposing
authorization and recognition endpoints for network-based policy queries.

Usage:
    python scripts/start_http_service.py [--host 127.0.0.1] [--port 5000] [--debug]

References:
    TRQP v2.0: https://trustoverip.github.io/tswg-trust-registry-protocol/
"""

import argparse
from pathlib import Path

try:
    from cawg_trqp_refimpl.http_service import HTTPTRQPService
except ImportError as e:
    print(f"Error: {e}")
    print("Ensure cawg-trqp-refimpl is installed: pip install -e .")
    exit(1)


def main() -> None:
    """Start HTTP service with CLI options."""
    parser = argparse.ArgumentParser(
        description="Start CAWG–TRQP HTTP service",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--policy-path",
        type=str,
        default="data/policies.json",
        help="Path to policies.json",
    )
    parser.add_argument(
        "--revocation-path",
        type=str,
        default="data/revocations.json",
        help="Path to revocations.json (optional)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Bind address",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Bind port",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable Flask debug mode",
    )

    args = parser.parse_args()

    # Validate paths
    policy_path = Path(args.policy_path)
    if not policy_path.exists():
        print(f"Error: Policy file not found: {args.policy_path}")
        exit(1)

    revocation_path = None
    if args.revocation_path:
        revocation_path = Path(args.revocation_path)
        if not revocation_path.exists():
            print(f"Warning: Revocation file not found: {args.revocation_path}")

    # Create and start service
    print(f"Starting TRQP HTTP service...")
    print(f"  Policy path: {policy_path}")
    if revocation_path:
        print(f"  Revocation path: {revocation_path}")
    print(f"  Address: http://{args.host}:{args.port}")
    print(f"  Debug mode: {args.debug}")
    print()
    print("Endpoints:")
    print(f"  POST /trqp/authorization")
    print(f"  POST /trqp/recognition")
    print(f"  GET /health")
    print()

    service = HTTPTRQPService(
        policy_path=policy_path,
        revocation_path=revocation_path,
        debug=args.debug,
    )

    service.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
