import json
from pathlib import Path
from jsonschema import Draft202012Validator


def test_performance_evidence_schema_accepts_complete_result():
    schema = json.loads(Path("schemas/performance-evidence.schema.json").read_text())
    evidence = {
        "scenario": "warm-cache-standard",
        "implementation_commit": "abc123",
        "workers": 8,
        "duration_seconds": 60,
        "requests": 600000,
        "throughput_rps": 10000,
        "latency_ms": {"p50": 0.45, "p95": 0.92, "p99": 1.34},
        "cache_hit_ratio": 0.999,
        "live_lookup_rate": 10,
        "errors": 0,
        "environment": {"cpu": "documented by operator"}
    }
    Draft202012Validator(schema).validate(evidence)


def test_benchmark_docs_disclaim_fixed_throughput():
    text = Path("benchmarks/README.md").read_text()
    assert "do **not** certify a fixed throughput" in text
