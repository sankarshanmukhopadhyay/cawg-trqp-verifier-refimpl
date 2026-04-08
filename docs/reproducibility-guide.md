# Reproducibility Guide

## Purpose

This repository now treats reproducibility as a first-class assurance concern. A verifier implementation should not only export an audit bundle, but also prove that the same request and policy inputs can regenerate the same expected artifact shape and outcome.

## Fixture

The canonical standard-profile reproducibility fixture is:

- `examples/reproducibility_bundle_standard.json`

It is generated from:

- `examples/verification_request.json`
- `data/policies.json`
- `data/revocations.json`
- fixed export timestamp `2026-03-31T00:00:00Z`

## Command

```bash
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
```

## What this checks

1. the verification result is reproducible for the supplied request
2. the audit bundle digest is stable
3. replay input policy sources are pinned
4. the expected fixture matches the regenerated bundle

## Why it matters

This gives implementers a compact mechanism for regression testing, cross-run comparison, and future cross-implementation exchange.
