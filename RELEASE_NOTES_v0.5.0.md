# v0.5.0 – Signed Offline Trust and C2PA-Style Manifest Ingestion

## Overview

This release closes the two most important realism gaps left open by v0.4.0.

First, offline edge verification no longer assumes that a snapshot is trustworthy merely because it exists. The verifier now checks an Ed25519 signature against a configured trust-anchor set and enforces snapshot expiry before using policy state.

Second, manifest ingestion no longer depends only on simplified repo fixtures. The parser now supports a C2PA-style JSON manifest-store envelope and extracts actor, issuer, action, resource, assertions, and provenance from that structure.

## What changed

### 1. Signed snapshot verification
- Added signature verification for `data/snapshot.json`
- Added `data/trust_anchors.json`
- Added expiry enforcement through `expires_at`
- Added explicit rejection outcomes for invalid or stale snapshots
- Added `scripts/sign_snapshot.py` for deterministic signing

### 2. C2PA-style manifest ingestion
- Added parser support for `manifest_store` JSON envelopes
- Added `examples/fixtures/cawg_manifest_c2pa.json`
- Updated fixture loading to route through parser output
- Preserved simplified fixture compatibility for demos and regression tests

### 3. Delivery hardening
- Added parser and snapshot validation tests
- Added `cryptography` dependency
- Added pytest source-path configuration
- Refreshed README, roadmap, integration guide, and repo tree

## Practical impact

This repo now behaves more credibly as a reference implementation in two places that matter operationally:

- **edge verification** now has a trustable offline policy source
- **manifest ingestion** now reflects a realistic C2PA-style structure instead of only a convenience fixture shape

## Next

The next release focus is v0.6.0:

- metrics and observability
- throughput and latency benchmarking
- edge and high-volume performance scenarios
