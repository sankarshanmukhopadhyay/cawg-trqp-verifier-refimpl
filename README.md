# CAWG–TRQP Reference Implementation

**Version:** v0.10.0  
**Status:** Reference implementation with deterministic audit bundles, replay tooling, multi-authority gateway routing, signed offline snapshots, and process-aware trust synthesis

## Overview

This repository demonstrates how **TRQP** can operate as the governance decision plane in a **CAWG/C2PA** verification workflow. The implementation now pushes beyond basic reference behavior into a more deterministic assurance profile:

- **deterministic audit bundles** with a stable serialization profile, canonical digest, and replay inputs
- **assurance-oriented validation and replay tooling** so exported bundles can be checked and re-executed
- **multi-authority trust gateway routing** for production-style interoperability patterns across distinct policy domains
- **process-aware trust synthesis** that binds content verification to actor authorization and process appraisal
- **signed snapshot support** for constrained and offline verification environments

## What this increment adds

### 1. Stable audit bundle serialization profile

Audit bundles now include:

- `bundle_profile`
- `bundle_version`
- `bundle_id`
- `bundle_digest_sha256`
- `replay_inputs`

This makes exported evidence portable, machine-checkable, and materially more deterministic across systems.

### 2. Validation and replay tooling

The repository now ships with:

- `schemas/audit-bundle.schema.json`
- `scripts/validate_audit_bundle.py`
- `scripts/replay_audit_bundle.py`

These support structural validation, digest verification, and replay against current policy data.

### 3. Multi-authority interoperability patterns

The trust gateway can now route requests deterministically by authority. The repository includes:

- `data/policies_multi_authority.json`
- `examples/interoperability_vector_multi_authority.json`
- route-aware gateway tests

This moves the implementation closer to real multi-registry and federated deployment topologies.

## Quick start

### Install

```bash
git clone <this-repo>
cd cawg-trqp-verifier-refimpl
pip install -e .
```

### Run standard verification

```bash
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_c2pa_pop.json \
  --profile standard
```

### Export a deterministic audit bundle

```bash
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_c2pa_pop.json \
  --profile standard \
  --use-gateway \
  --exported-at 2026-03-31T00:00:00Z \
  --export-audit-bundle examples/exported_audit_bundle.json
```

### Validate an audit bundle

```bash
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.json
```

### Replay an audit bundle

```bash
python scripts/replay_audit_bundle.py \
  examples/exported_audit_bundle.json \
  --policies data/policies.json \
  --revocations data/revocations.json
```

### Start HTTP service

```bash
python scripts/start_http_service.py --port 5000
```

## Verification profiles

| Profile | Network posture | Policy source | Process posture | Primary use case |
|---|---|---|---|---|
| `edge` | intermittent or offline | signed snapshot only | local appraisal from supplied evidence | handheld, constrained, disconnected verification |
| `standard` | stable | cache-first with live lookup on miss | policy-aware composite decision | service and platform verification |
| `high_assurance` | stable | live lookup always | strict process policy enforcement | regulated or audit-sensitive verification |

## Deterministic assurance model

The implementation now treats exported evidence as a machine-verifiable artifact rather than a convenience log.

Each audit bundle can now answer four operational questions:

1. **What request was evaluated?** via `request_summary` and `replay_inputs.request`
2. **What decision was reached?** via `verification_result`
3. **What evidence and policy epoch supported it?** via `policy_evidence`
4. **Can the result be validated and replayed?** via bundle schema validation, digest verification, and replay tooling

## Documentation map

- `docs/INTEGRATION_GUIDE.md`
- `docs/architecture.md`
- `docs/audit-bundle-profile.md`
- `docs/deployment-guide.md`
- `docs/http-transport-patterns.md`
- `docs/interoperability-vectors.md`
- `docs/trust-gateway.md`
- `docs/verifier-profiles.md`
- `docs/NON_TECHNICAL_OVERVIEW.md`

## Roadmap status

The prior next-horizon items are now implemented in this working tree:

- stabilize audit bundle serialization profile
- add assurance-oriented bundle validation and replay tooling
- expand interoperability vectors toward multi-authority production patterns

The next meaningful increment should focus on signed bundle attestations, externalized policy feeds, and cross-run reproducibility fixtures.

## Validation

```bash
pytest -q
```

Current repository test status for this increment:

- **25 passed**
- **5 skipped**

The skipped tests are optional Flask-dependent paths.
