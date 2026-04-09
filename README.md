# CAWG–TRQP Reference Implementation

**Version:** v0.12.0  
**Status:** Release candidate for executable verification profiles and assurance overlays

## Overview

This repository demonstrates how **TRQP** can operate as the governance decision plane in a **CAWG/C2PA** verification workflow. In `v0.12.0`, verification profiles move from simple runtime presets to **machine-readable enforcement contracts**. The verifier now resolves a profile, applies optional assurance overlays, enforces the resulting controls at runtime, and carries the resolved profile into exported evidence.

That shift matters because policy execution now produces portable evidence about:

- what authority posture was enforced
- how freshness and revocation were handled
- whether degraded policy conditions failed open or failed closed
- what evidence obligations applied to exported audit artifacts
- whether the result can be replayed deterministically

## What v0.12.0 adds

### 1. Executable verification profiles

Profiles are now first-class JSON artifacts validated by `schemas/verification-profile.schema.json` and loaded through `src/cawg_trqp_refimpl/profile.py`.

### 2. Assurance overlays

A base profile can now be tightened with overlays such as:

- `freshness_strict`
- `evidence_attested`

This avoids profile sprawl while still making stricter controls machine-verifiable.

### 3. Profile-aware audit bundles and replay

Exported audit bundles now carry the **resolved profile object** in `replay_inputs.profile`. Replay tooling uses that profile directly, so downstream systems can re-run the same governance contract instead of inferring behavior from surrounding context.

### 4. Fail-open / fail-closed enforcement semantics

Profiles now explicitly govern degraded-policy behavior. For example:

- `standard` defers when live policy is unavailable
- `high_assurance` rejects when live policy is unavailable

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

### Replay using the resolved profile embedded in the bundle

```bash
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
```

### Check reproducibility fixture

```bash
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
```

## Verification profiles

| Profile | Base posture | Authority policy | Failure policy | Evidence posture | Determinism posture |
|---|---|---|---|---|---|
| `edge` | signed snapshot only | trust anchors required | fail-open on live network absence, because no live network is expected | audit export optional but not required | replay not required |
| `standard` | cache-first with live fallback | permissive recognition posture | fail-open / defer on policy outage | audit bundle export supported | replayable |
| `high_assurance` | live policy only | trust anchors required and untrusted recognition blocked | fail-closed on policy outage | audit bundle export plus attestation required | pinned-feed replay required |

## Assurance overlay model

The governing unit is now:

```text
verification_profile = base_profile + assurance_overlay(s)
```

This lets the repository express stricter semantics without multiplying profile names.

## Repository structure relevant to v0.12.0

- `profiles/` — built-in executable profiles
- `profiles/overlays/` — assurance overlays
- `schemas/verification-profile.schema.json` — profile schema
- `src/cawg_trqp_refimpl/profile.py` — loader, validation, overlay merge logic
- `docs/verifier-profiles.md` — profile semantics and usage
- `tests/test_profiles.py` — assurance-oriented profile tests

## Documentation map

- `docs/architecture.md`
- `docs/audit-bundle-profile.md`
- `docs/release-assets.md`
- `docs/release-readiness.md`
- `docs/reproducibility-guide.md`
- `docs/trust-gateway.md`
- `docs/verifier-profiles.md`
- `docs/repo-tree.md`

## Validation

```bash
pytest -q
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
```

## Roadmap direction after v0.12.0

This release establishes the control plane needed for:

- transport-specific policy feed constraints
- revocation freshness assertions and delta channels
- cross-implementation exchange of profile-bound audit fixtures
- alignment with external conformance and assurance suites
