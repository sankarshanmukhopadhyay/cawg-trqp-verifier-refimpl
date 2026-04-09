# Verification Profiles

## Purpose

Verification profiles are now **machine-readable governance contracts**. They define how the verifier should behave under normal and degraded conditions, and they travel with exported evidence so downstream systems can reproduce the same decision contract.

## Model

```text
verification_profile = base_profile + assurance_overlay(s)
```

A profile resolves to six control domains:

- `authority`
- `freshness`
- `revocation`
- `failure`
- `evidence`
- `determinism`

The schema for these controls is defined in `schemas/verification-profile.schema.json`.

## Built-in base profiles

### `edge`

Use when verification must work from signed snapshots in disconnected or bandwidth-constrained settings.

Key controls:

- trust anchors required
- snapshot revocation posture
- no requirement to emit replayable evidence

### `standard`

Use when verification is service-backed and cache-first behavior is acceptable.

Key controls:

- permissive authority posture
- live lookup on cache miss
- fail-open / defer on policy unavailability
- replayable evidence supported

### `high_assurance`

Use when verification must fail closed under degraded policy conditions and produce attestable evidence.

Key controls:

- trust anchors required
- live-only freshness posture
- hard-fail revocation handling
- attested audit bundles required
- pinned-feed replay required

## Overlays

Overlays let an implementer tighten controls without inventing a new profile name.

### Included overlays

- `freshness_strict` — require live policy and fail closed when policy is unavailable
- `evidence_attested` — require emitted audit bundles to be attested

## CLI usage

```bash
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_c2pa_pop.json \
  --profile standard \
  --overlay freshness_strict \
  --overlay evidence_attested
```

## Audit bundle behavior

When a verification result is exported as an audit bundle, the **resolved** profile object is copied into `replay_inputs.profile`.

That means replay no longer depends on local assumptions such as:

- which profile name was intended
- whether overlays were applied
- whether strict evidence or freshness controls were active

## Assurance posture

Profiles can now be tested directly for:

- trust-anchor requirements
- live policy requirements
- fail-open / fail-closed semantics
- evidence obligations
- replayability expectations
