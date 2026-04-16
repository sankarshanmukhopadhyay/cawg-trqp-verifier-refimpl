# Reproducibility Guide

## Canonical bundle

The canonical reproducibility fixture remains:

- `examples/reproducibility_bundle_standard.json`

## What changed in v0.13.0

Replay now includes more than the request, profile, and pinned feeds.

The bundle also carries:

- transport metadata
- revocation status
- a replay contract describing whether transport checks passed and whether revocation freshness was evaluated

## Why that matters

Reproducibility is stronger when another implementation can compare not just the decision outcome, but also the input trust posture asserted by the original run.

## Cross-implementation fixture package

The repository now includes a canonical exchange package:

- `fixtures/profile-bound/standard-v1/`

This package is intended to be portable across implementations.

## Commands

```bash
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
```
