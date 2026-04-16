# Reproducibility Guide

## Canonical replay bundle

The canonical reproducibility bundle remains:

- `examples/reproducibility_bundle_standard.json`

This is the fastest way to test whether the same request, profile, feeds, and replay contract yield the same result surface.

## What reproducibility now covers

Replay now includes more than the request, profile, and pinned feeds.

The bundle also carries:

- transport metadata
- revocation status
- a replay contract describing whether transport checks passed and whether revocation freshness was evaluated

## Fixture exchange alongside replay

The repository now also carries canonical fixture exchange packages:

- `fixtures/profile-bound/standard-v1/`
- `fixtures/profile-bound/high-assurance-v1/`
- `fixtures/profile-bound/gateway-standard-v1/`
- `fixtures/profile-bound/multi-authority-v1/`

These packages are useful when another implementation needs a stable exchange artifact without first consuming the entire audit-bundle flow.

## Recommended usage

Use the reproducibility bundle when you want to confirm that a concrete audit artifact still replays correctly.

Use the fixture packages when you want to compare multiple implementations against a stable expected-result contract.

## Commands

```bash
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
python scripts/validate_examples.py
```
