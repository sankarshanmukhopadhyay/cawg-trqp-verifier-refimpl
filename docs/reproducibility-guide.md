---
layout: default
title: "Reproducibility Guide"
description: "Canonical replay bundles and deterministic re-verification."
parent: "Assurance & Evidence"
nav_order: 4
---
# Reproducibility Guide

## Canonical replay bundle

The historically published reproducibility bundle is:

- `examples/reproducibility_bundle_standard.json`

**Compatibility limitation:** this immutable bundle records a revocation-feed issue time later than the evaluation date and therefore asserts `fresh` under obsolete verifier behavior. The corrected implementation appropriately reports `stale_but_warned` for that evidence. The archive remains useful for demonstrating a semantic change, but must **not** be presented as a passing current replay or as evidence of present authorization freshness. The original bundle identity is retained.

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

Use the historical bundle to examine reproducibility boundaries and the explicitly documented pre/post-hardening difference. For a positive, genuinely fresh replay with an explicitly pinned evaluation instant, run the targeted regression test listed below.

Use fixture packages to compare implementations, but account for the declared evaluation time and any documented semantic compatibility change. A signed descriptor alone does not validate a future-issued revocation feed.

## Commands

```bash
python scripts/validate_legacy_replay_freshness.py
pytest -q tests/test_cache_revocation_consistency.py
python scripts/validate_examples.py
make validate
```


The legacy validation command asserts a *known, bounded incompatibility* on a pinned assessment clock. Running `python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .` directly with the hardened verifier is expected to report differences, not to pass. Preserve these differences for forensic review rather than changing signed historical evidence to obtain a green replay.
