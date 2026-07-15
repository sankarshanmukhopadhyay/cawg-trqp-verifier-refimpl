## Unreleased

- No unreleased changes.

# Changelog

## Unreleased

### Changed

- Establishes a Tier 1 flagship repository contract with explicit authority boundaries, machine-readable portfolio metadata, a common validation entry point, citation metadata, and a documented TRQP adoption path.
- Adds CI enforcement for required governance, adoption, evidence, and documentation artifacts without creating a new release.

## v0.16.0

- Restored full validation health across schemas, feed descriptors, audit bundles, replay bundles, the photography contest walkthrough, and tests.
- Added explicit descriptor policy controls with observe, warn, and fail semantics by feed type.
- Added external assurance-suite ingestion through `conformance/assurance-suite-manifest.json` and `scripts/export_conformance_pack.py`.
- Added parser adapter contract for future binary CAWG/C2PA extraction.
- Added structured HTTP audit events for verification and audit-bundle routes.
- Added release checksum tooling and `release-assets/checksums-v0.16.0.json`.
- Refreshed signed snapshot evidence, profile-bound fixture packages, expected results, audit bundles, and replay bundles.
- Rewrote README and roadmap content for the current assurance posture.

## v0.15.0

- Hardened HTTP request handling with content-type, request-size, typed-field, and safe profile-resolution checks.
- Added safe API profile loading so HTTP callers cannot resolve arbitrary local profile paths.
- Added high-assurance fail-closed behavior for missing or invalid policy and revocation feed descriptor evidence.
- Hardened feed descriptor validation for malformed descriptors, malformed timestamps, invalid base64, and invalid Ed25519 signature lengths.
- Extended audit bundles to preserve policy, revocation, descriptor, and trust-anchor source digests for deterministic replay.
- Hardened audit replay with trusted-root path boundaries and pinned feed digest validation before use.
- Added security regression tests covering unsafe API profile references, non-JSON requests, missing descriptors, malformed descriptors, replay path boundaries, and replay digest mismatch.
- Updated roadmap, compatibility matrix, README, release readiness notes, and version metadata for the v0.15.0 release.

## v0.14.0

- Added signed feed descriptor and feed attestation schemas.
- Added signed example descriptors for policy, revocation, snapshot, and gateway route feeds.
- Added runtime feed descriptor validation and evidence export.
- Added stable freshness and descriptor reason codes.
- Added audit/replay propagation for feed descriptor evidence.
- Added descriptor validation script and conformance tests.

## v0.13.0

- add transport controls to verification profiles
- add revocation freshness controls with warn/fail semantics and delta/live expectations
- evaluate transport and revocation posture during verification runtime
- extend audit bundle replay inputs with transport metadata, revocation status, and replay contract fields
- add canonical profile-bound fixture package for cross-implementation exchange
- refresh example bundles, reproducibility artifacts, and documentation
- add tests covering transport guardrails, revocation freshness behavior, and fixture completeness

## v0.12.0

- formalize verification profiles as schema-validated JSON artifacts
- add assurance overlays to tighten enforcement semantics without adding profile sprawl
- enforce fail-open and fail-closed behavior from profile controls
- embed resolved profile objects into audit bundles and replay workflows
- add profile tests covering overlay application and degraded-policy behavior
- `RELEASE_NOTES_v0.12.0.md`

## v0.11.0

- add optional Ed25519 bundle attestation
- pin external policy and revocation feeds in replay metadata
- add deterministic reproducibility fixture and comparison tooling

## Earlier releases

See the version-specific release notes in the repository root for historical milestones.
