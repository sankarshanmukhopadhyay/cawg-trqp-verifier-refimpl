# Roadmap

## Completed in v0.5.0

1. Replace simplified fixture-only parsing with a parser that also handles C2PA-style manifest-store JSON.
2. Add signed policy snapshot verification with trust-anchor validation and expiry enforcement.

## Next up: v0.6.0

1. Add metrics and observability hooks for cache hit rate, live lookup volume, and snapshot-validation outcomes.
2. Add throughput and latency benchmarking for edge, standard, and high_assurance profiles.
3. Add benchmark fixtures for low-bandwidth, high-volume, and constrained-device scenarios.

## After that: v0.7.0

1. Production hardening and deployment guide.
2. Trust gateway component for remote policy mediation.
3. Richer audit bundle generation and export.
