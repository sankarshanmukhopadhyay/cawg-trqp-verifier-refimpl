# CAWG–TRQP Reference Implementation

**Version:** v0.11.0  
**Status:** Release candidate focused on attestable audit bundles, pinned replay sources, and reproducibility fixtures

## Overview

This repository demonstrates how **TRQP** can operate as the governance decision plane in a **CAWG/C2PA** verification workflow. The current increment strengthens the evidence layer so exported verification artifacts can be signed, replayed against pinned policy sources, and compared across runs.

The result is a more operational assurance profile for content verification systems that need machine-verifiable evidence rather than ad hoc logs.

## What v0.11.0 adds

### 1. Signed audit bundle attestation

Audit bundles can now carry an optional `bundle_attestation` block signed with Ed25519. This allows exported evidence artifacts to be independently verified after transport, storage, or handoff.

### 2. Externalized policy feed pinning

Replay inputs now carry a `policy_feed` descriptor with pinned policy and revocation sources plus content digests. Replay tooling can use those sources directly, making bundle re-execution materially more portable.

### 3. Reproducibility fixture workflow

The repository now includes deterministic reproducibility tooling so implementers can regenerate a known-good bundle and compare it byte-for-byte at the data model level.

## Quick start

### Install

```bash
git clone <this-repo>
cd cawg-trqp-verifier-refimpl
pip install -e .
```

### Run standard verification

```bash
python -m cawg_trqp_refimpl.cli   --fixture examples/fixtures/cawg_manifest_c2pa_pop.json   --profile standard
```

### Export a deterministic audit bundle

```bash
python -m cawg_trqp_refimpl.cli   --fixture examples/fixtures/cawg_manifest_c2pa_pop.json   --profile standard   --use-gateway   --exported-at 2026-03-31T00:00:00Z   --export-audit-bundle examples/exported_audit_bundle.json
```

### Export and sign an audit bundle

```bash
python -m cawg_trqp_refimpl.cli   --fixture examples/fixtures/cawg_manifest_c2pa_pop.json   --profile standard   --exported-at 2026-03-31T00:00:00Z   --export-audit-bundle examples/exported_audit_bundle.signed.json   --bundle-signing-key data/snapshot_signing_key.example.pem   --bundle-key-id media-registry-snapshot-key-1
```

### Validate an audit bundle and its attestation

```bash
python scripts/validate_audit_bundle.py   examples/exported_audit_bundle.signed.json   --trust-anchors data/trust_anchors.json
```

### Replay using pinned policy feed metadata

```bash
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
```

### Check reproducibility fixture

```bash
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
```

## Verification profiles

| Profile | Network posture | Policy source | Process posture | Primary use case |
|---|---|---|---|---|
| `edge` | intermittent or offline | signed snapshot only | local appraisal from supplied evidence | handheld, constrained, disconnected verification |
| `standard` | stable | cache-first with live lookup on miss | policy-aware composite decision | service and platform verification |
| `high_assurance` | stable | live lookup always | strict process policy enforcement | regulated or audit-sensitive verification |

## Assurance model

Each audit bundle can now answer six operational questions:

1. **What request was evaluated?** via `request_summary` and `replay_inputs.request`
2. **What decision was reached?** via `verification_result`
3. **What evidence and policy epoch supported it?** via `policy_evidence`
4. **What policy sources were pinned for replay?** via `replay_inputs.policy_feed`
5. **Can the artifact be independently attested?** via `bundle_attestation`
6. **Can the result be reproduced?** via validation, replay, and reproducibility fixture tooling

## Documentation map

- `docs/INTEGRATION_GUIDE.md`
- `docs/architecture.md`
- `docs/audit-bundle-profile.md`
- `docs/reproducibility-guide.md`
- `docs/deployment-guide.md`
- `docs/http-transport-patterns.md`
- `docs/interoperability-vectors.md`
- `docs/trust-gateway.md`
- `docs/verifier-profiles.md`
- `docs/NON_TECHNICAL_OVERVIEW.md`

## Roadmap status

v0.11.0 completes substantial portions of the current next horizon by introducing:

- signed bundle attestation for exported verification artifacts
- pinned external policy feed metadata for replay portability
- reproducibility fixtures for cross-run comparison

The next release should focus on richer feed transports, delta update channels, and cross-implementation fixture exchange.

## Validation

```bash
pytest -q
```
