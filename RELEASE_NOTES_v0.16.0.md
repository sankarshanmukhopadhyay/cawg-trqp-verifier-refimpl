---
layout: default
title: "Release Notes v0.16.0"
parent: "Releases"
nav_order: 13
---
# Release Notes: v0.16.0

## Release Theme

v0.16.0 is a roadmap-closure and assurance-hardening release. It turns the repository from a strong verifier reference into a cleaner conformance and evidence handoff surface.

The release resolves contract drift across code, schemas, fixtures, replay bundles, and documentation. It also completes the practical roadmap items around external assurance-suite ingestion, descriptor policy configuration, parser adapter boundaries, operational hardening, and release asset integrity.

## Highlights

- Restored full validation health: examples, feed descriptors, audit bundles, replay bundles, photography contest walkthrough, conformance export, checksum export, and tests all pass.
- Added `controls.descriptor_policy` to verification profiles with per-feed `observe`, `warn`, and `fail` behavior.
- Added `conformance/assurance-suite-manifest.json` for external conformance and assurance-suite ingestion.
- Added `src/cawg_trqp_refimpl/manifest_adapters.py` to preserve a stable parser signal contract while leaving room for future binary CAWG/C2PA extraction.
- Added structured HTTP audit events for verification and audit-bundle routes.
- Added release checksum tooling and `release-assets/checksums-v0.16.0.json`.
- Refreshed signed snapshot, profile-bound fixtures, expected results, audit bundles, replay bundles, and photography contest evidence.
- Rewrote the README and roadmap around current repository behavior instead of historical release fragments.

## Code Changes

- `src/cawg_trqp_refimpl/profile.py`
  - Added default `descriptor_policy` controls.
  - Preserves backward compatibility for inline profiles through default control merging.

- `src/cawg_trqp_refimpl/verifier.py`
  - Evaluates feed descriptor failures through explicit profile policy.
  - Preserves high-assurance fail-closed behavior for required descriptors.

- `src/cawg_trqp_refimpl/http_service.py`
  - Emits structured JSON audit events for verification and audit-bundle operations.

- `src/cawg_trqp_refimpl/manifest_adapters.py`
  - Adds `ManifestParserAdapter`, `JsonManifestAdapter`, and reserved `C2PABinaryManifestAdapter`.

## Schema and Profile Changes

- `schemas/verification-profile.schema.json`
  - Adds required `controls.descriptor_policy`.

- `profiles/standard.json`
  - Observes descriptor evidence.

- `profiles/high_assurance.json`
  - Fails on policy, revocation, and gateway-route descriptor defects.

- `profiles/edge.json`
  - Fails on snapshot descriptor policy when configured.

## Conformance and Assurance Artifacts

- Added `conformance/assurance-suite-manifest.json`.
- Updated `conformance/compatibility-matrix.json` to v0.16.0.
- Refreshed `fixtures/profile-bound/*/resolved_profile.json`.
- Refreshed `fixtures/profile-bound/*/expected_result.json`.
- Added `scripts/export_conformance_pack.py`.
- Added `scripts/generate_release_checksums.py`.
- Added `release-assets/checksums-v0.16.0.json`.

## Documentation Changes

- Rewrote `README.md`.
- Rewrote `ROADMAP.md`.
- Added `docs/assurance-suite-ingestion.md`.
- Added `docs/parser-adapter-contract.md`.
- Added `docs/descriptor-policy.md`.
- Added `docs/operational-hardening.md`.
- Updated issue files to show closure or partial closure status.

## Validation

The release was validated with:

```bash
python scripts/validate_examples.py
python scripts/validate_feed_descriptors.py
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
python scripts/validate_photography_contest_example.py
python scripts/export_conformance_pack.py --check
python scripts/generate_release_checksums.py --check
pytest -q
```

Result:

```text
68 passed
```

## Upgrade Notes

Profile JSON now includes `controls.descriptor_policy`. Inline profiles that omit the field continue to work because defaults are merged at runtime, but committed profile artifacts should include the explicit control.

High-assurance verification still fails closed when required policy or revocation feed descriptors are missing or invalid. Positive high-assurance fixtures now provide valid descriptor evidence.
