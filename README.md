# CAWG–TRQP Reference Implementation

**Version:** v0.13.0  
**Status:** Release candidate for deterministic input trust and replay fidelity

## Overview

This repository shows how **TRQP** can serve as the governance decision plane in a **CAWG/C2PA** verification workflow.

In `v0.13.0`, the verifier stops treating policy inputs as ambient infrastructure. Profiles now govern not only how a decision is made, but also what kind of feed transport is acceptable, how fresh revocation material must be, and what replay evidence must travel with the outcome.

That matters because a verifier that cannot account for the reliability of its own inputs is still operating on trust assumptions it cannot evidence.

## What v0.13.0 adds

### 1. Transport-aware verification profiles

Profiles can now declare transport requirements for policy feeds:

- `mode`: `http`, `gateway`, or `local`
- `integrity`: `none`, `tls`, or `signed`
- `availability_requirement`: `best_effort` or `required`

The verifier evaluates the runtime transport posture and records the result in policy evidence and replay inputs.

### 2. Revocation freshness enforcement

Profiles now declare revocation freshness expectations:

- maximum acceptable age
- warn vs fail behavior
- whether delta/live channel semantics are required

This makes revocation handling explicit, testable, and exportable.

### 3. Replay fidelity extensions

Audit bundles now carry:

- transport metadata
- revocation status and freshness evaluation
- a replay contract stating whether deterministic inputs were present

Replay is no longer just “run it again with the same profile.” It now captures whether the verifier believed its inputs were trustworthy enough at decision time.

### 4. Canonical profile-bound fixtures

The repository now includes a canonical fixture package under `fixtures/profile-bound/standard-v1/` containing:

- the request
- the resolved profile
- the expected result
- pinned policy and revocation feeds
- a fixture manifest for cross-implementation exchange

### 5. Documentation refresh

The documentation has been updated to explain deterministic input trust in both technical and non-technical terms, including transport constraints, revocation freshness, replay fidelity, and alignment directions for broader TRQP assurance work.

## Quick start

### Install

```bash
git clone <this-repo>
cd cawg-trqp-refimpl
pip install -e .
```

### Run standard verification

```bash
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_c2pa_pop.json \
  --profile standard
```

### Run high assurance verification with attested evidence export

```bash
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_c2pa_pop.json \
  --profile high_assurance \
  --exported-at 2026-04-09T00:00:00Z \
  --export-audit-bundle examples/exported_audit_bundle.signed.json \
  --bundle-signing-key data/snapshot_signing_key.example.pem \
  --bundle-key-id media-registry-snapshot-key-1
```

### Apply overlays to a base profile

```bash
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_c2pa_pop.json \
  --profile standard \
  --overlay freshness_strict \
  --overlay evidence_attested \
  --exported-at 2026-04-09T00:00:00Z \
  --export-audit-bundle examples/exported_audit_bundle.signed.json \
  --bundle-signing-key data/snapshot_signing_key.example.pem \
  --bundle-key-id media-registry-snapshot-key-1
```

### Validate an audit bundle and its attestation

```bash
python scripts/validate_audit_bundle.py \
  examples/exported_audit_bundle.signed.json \
  --trust-anchors data/trust_anchors.json
```

### Replay an audit bundle

```bash
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
```

### Check deterministic reproducibility

```bash
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
```

## Verification profiles

| Profile | Base posture | Transport posture | Revocation posture | Failure policy | Evidence posture |
|---|---|---|---|---|---|
| `edge` | signed snapshot only | local signed data | snapshot-based, warning semantics | fail-open on network absence because no live network is expected | audit export optional |
| `standard` | cache-first with live fallback | HTTP/TLS accepted, gateway compatible | delta-oriented with warning semantics | fail-open / defer on policy outage | audit bundle export supported |
| `high_assurance` | live policy only | live transport required | hard-fail freshness semantics with delta/live expectations | fail-closed on policy outage | audit bundle export plus attestation required |

## Canonical fixture package

The fixture exchange surface for `v0.13.0` is:

```text
fixtures/
  profile-bound/
    standard-v1/
      manifest.json
      request.json
      resolved_profile.json
      expected_result.json
      pinned_feeds/
        policies.json
        revocations.json
```

## Repository structure relevant to v0.13.0

- `profiles/` — executable verification profiles
- `profiles/overlays/` — assurance overlays
- `fixtures/profile-bound/` — canonical fixture exchange packages
- `schemas/verification-profile.schema.json` — profile schema with transport and revocation controls
- `schemas/audit-bundle.schema.json` — replay fidelity and audit bundle schema
- `src/cawg_trqp_refimpl/transport.py` — transport constraint evaluation
- `src/cawg_trqp_refimpl/verifier.py` — transport and revocation enforcement
- `src/cawg_trqp_refimpl/replay.py` — replay fidelity comparison
- `docs/deterministic-input-trust.md` — control-plane explanation of the new theme

## Documentation map

- `docs/NON_TECHNICAL_OVERVIEW.md`
- `docs/architecture.md`
- `docs/audit-bundle-profile.md`
- `docs/deterministic-input-trust.md`
- `docs/release-assets.md`
- `docs/release-readiness.md`
- `docs/reproducibility-guide.md`
- `docs/trqp-alignment.md`
- `docs/verifier-profiles.md`
- `docs/repo-tree.md`

## Validation

```bash
pytest -q
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
```

## Completed in v0.13.0

This release completes the `v0.12.0` roadmap items for:

- transport-specific policy feed constraints
- revocation freshness assertions and delta-channel semantics
- cross-implementation exchange of profile-bound audit fixtures
- first alignment surface for broader TRQP assurance and conformance work

## Next roadmap direction after v0.13.0

The next practical increment should focus on:

- signed remote feed descriptors and stronger transport attestation
- explicit freshness breach reason codes in exported evidence
- fixture exchange for multiple profiles, including high-assurance and gateway-mediated cases
- direct alignment hooks into external TRQP conformance and assurance suites


## Maintenance hardening after v0.13.0

The current build also hardens publication and conformance surfaces by assigning stable schema/profile URIs, validating shipped examples and fixtures in CI, consolidating revocation freshness evaluation into a single path, documenting transport compatibility asymmetry, and bounding cache growth with LRU eviction.
