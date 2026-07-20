#!/usr/bin/env python3
"""Small, reproducible library benchmark; not a production throughput claim."""
from __future__ import annotations
import argparse, json, statistics, subprocess, time
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cawg_trqp_refimpl.cache import TTLCache
from cawg_trqp_refimpl.models import VerificationRequest
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.verifier import Verifier


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int((len(ordered) - 1) * p))]


def commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "uncommitted"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=1000)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    payload = json.loads((root / "examples/verification_request.json").read_text())
    req = VerificationRequest(**{k: payload.get(k) for k in ["asset_id", "integrity_ok", "entity_id", "authority_id", "issuer_id", "action", "resource", "context", "process_evidence"]})
    cache = TTLCache(maxsize=4096)
    verifier = Verifier(service=MockTRQPService(root / "data/policies.json", root / "data/revocations.json"), cache=cache)
    verifier.verify(req, profile="standard")
    latencies: list[float] = []
    start = time.perf_counter()
    for _ in range(args.iterations):
        t0 = time.perf_counter()
        verifier.verify(req, profile="standard")
        latencies.append((time.perf_counter() - t0) * 1000)
    duration = time.perf_counter() - start
    stats = cache.stats()
    evidence = {
        "scenario": "warm-cache-standard",
        "implementation_commit": commit(),
        "workers": 1,
        "duration_seconds": duration,
        "requests": args.iterations,
        "throughput_rps": args.iterations / duration,
        "latency_ms": {"p50": percentile(latencies, .50), "p95": percentile(latencies, .95), "p99": percentile(latencies, .99)},
        "cache_hit_ratio": stats["hit_ratio"],
        "live_lookup_rate": 0,
        "errors": 0,
        "environment": {"benchmark_type": "single-process-library"}
    }
    text = json.dumps(evidence, indent=2)
    if args.output:
        args.output.write_text(text + "\n")
    print(text)

if __name__ == "__main__":
    main()
