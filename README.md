# CAWG–TRQP Reference Implementation

**Version:** v0.5.0  
**Status:** Reference implementation with signed offline snapshots and C2PA-style JSON manifest ingestion

## Overview

This repository demonstrates, in executable form, how **TRQP** operates as the **governance decision plane** in a **CAWG/C2PA** verification workflow.

The architectural split is deliberate:

- **CAWG/C2PA** provides content-bound provenance and assertion packaging
- **Identity material** provides actor and issuer binding
- **TRQP** provides authorization and issuer-recognition answers
- **This verifier** synthesizes the final trust decision across online, cached, and offline modes

v0.5.0 focuses on the two most material roadmap items from v0.4.0: **signed snapshot verification** for offline trust and **real C2PA-style JSON manifest parsing** for higher-fidelity ingestion.

## What v0.5.0 Adds

### Signed snapshot verification

- Ed25519 signature verification for offline policy snapshots
- Trust-anchor model in `data/trust_anchors.json`
- Snapshot freshness and expiry enforcement through `expires_at`
- Explicit rejection path for tampered, unsigned, stale, or unknown-signer snapshots
- `scripts/sign_snapshot.py` to generate or refresh detached snapshot signatures

### C2PA-style manifest ingestion

- Parser now handles both simplified fixtures and **C2PA-style manifest-store JSON envelopes**
- Signal extraction includes:
  - actor identifier
  - issuer identifier
  - credential type
  - action and resource
  - provenance chain
  - assertion set
- `fixture_loader.py` now uses the parser output instead of a fixture-specific shortcut path

### Delivery hardening

- Test coverage expanded around signed snapshots and parser behavior
- `pytest` import path configuration added in `pyproject.toml`
- Versioning, docs, examples, and repo tree refreshed for v0.5.0

## Quick Start

### Install

```bash
git clone <this-repo>
cd cawg-trqp-verifier-refimpl
pip install -e .
```

### Run standard verification

```bash
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_minimal.json \
  --profile standard
```

### Run edge verification with signed snapshot

```bash
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_c2pa.json \
  --profile edge \
  --snapshot data/snapshot.json \
  --trust-anchors data/trust_anchors.json
```

### Start HTTP TRQP service

```bash
python scripts/start_http_service.py --port 5000
```

### Re-sign a snapshot

```bash
python scripts/sign_snapshot.py \
  data/snapshot.json \
  data/snapshot_signing_key.example.pem \
  --key-id media-registry-snapshot-key-1
```

## Verification Profiles

| Profile | Network posture | Policy source | Primary use case |
|---|---|---|---|
| `edge` | intermittent or offline | signed snapshot only | handheld, constrained, disconnected verification |
| `standard` | stable | cache-first with live lookup on miss | service and platform verification |
| `high_assurance` | stable | live lookup always | regulated or audit-sensitive verification |

## Parser Modes

| Mode | Input shape | Purpose |
|---|---|---|
| `fixture` | simplified repo fixture | deterministic tests and quick demos |
| `c2pa_json` | C2PA-style manifest-store JSON | higher-fidelity CAWG/C2PA ingestion |

## Architecture

```text
CAWG/C2PA Manifest or Manifest Store
    ↓ extract actor, issuer, action, resource, assertions, provenance
Identity Material
    ↓ bind issuer and actor context
TRQP Query Layer
    ↓ authorization + recognition + revocation signals
Verifier
    ↓ synthesize mode-specific trust decision
VerificationResult
```

For the edge profile, the policy path is:

```text
Signed Snapshot → Trust Anchor Verification → Freshness Check → Offline Authorization/Recognition → Trust Decision
```

## Repository Structure

See `docs/repo-tree.md` for the refreshed tree and `docs/INTEGRATION_GUIDE.md` for the end-to-end workflow.

## Current Priorities

v0.5.0 closes the two largest realism gaps from earlier releases:

1. offline snapshot provenance is now verified instead of assumed
2. manifest ingestion now supports a C2PA-style JSON structure instead of only simplified fixtures

The next release track now moves to **metrics, observability, and performance benchmarking**.
