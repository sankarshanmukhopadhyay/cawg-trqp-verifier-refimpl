#!/usr/bin/env python3
"""HTTP smoke benchmark using Flask's test client; not a production server benchmark."""
from __future__ import annotations
import argparse, json, time
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cawg_trqp_refimpl.http_service import HTTPTRQPService


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=100)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    service = HTTPTRQPService(root / "data/policies.json", root / "data/revocations.json")
    client = service.app.test_client()
    payload = json.loads((root / "examples/verification_request.json").read_text())
    start = time.perf_counter()
    errors = 0
    for _ in range(args.iterations):
        if client.post("/trqp/verify", json=payload).status_code != 200:
            errors += 1
    duration = time.perf_counter() - start
    print(json.dumps({"requests": args.iterations, "duration_seconds": duration, "throughput_rps": args.iterations / duration, "errors": errors, "cache": service.cache.stats()}, indent=2))

if __name__ == "__main__":
    main()
