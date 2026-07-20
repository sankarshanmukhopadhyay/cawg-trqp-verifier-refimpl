# Performance and scale evidence

These scripts make scale claims testable. They do **not** certify a fixed throughput and the Flask test client is not a production server.

```bash
python benchmarks/benchmark_verifier.py --iterations 10000 --output performance-evidence.json
python benchmarks/benchmark_http.py --iterations 1000
```

A publishable result must identify hardware, worker count, process model, cache topology, request mix, cache-hit ratio, registry latency, evidence mode, duration, errors, and the exact commit. Validate exported evidence against `schemas/performance-evidence.schema.json`.
