---
layout: default
title: "Changelog"
parent: "Releases"
nav_order: 1
---
# Changelog

## Unreleased

### Added

- GitHub Pages documentation site rebuilt on the Just the Docs theme, covering every existing document under an audience-organized navigation (Start Here, Architecture & Deployment, Implementation Guides, Assurance & Evidence, Interoperability, Walkthroughs, Governance & Policy, Releases).
- `docs/PRESENTATION_BRIEF.md`, a speaker-ready ten-minute walkthrough for external presentations.
- `.github/ISSUE_TEMPLATE/` (bug report, adoption/interoperability report) and `.github/pull_request_template.md`.
- `.github/dependabot.yml` for Python and GitHub Actions dependency updates.
- `.github/workflows/pages.yml` to build and deploy the documentation site on every push to `main`.
- `.github/workflows/pypi-publish.yml` implementing the PyPI publication step previously described in the v0.17.0 release notes but not present as a workflow file.

### Fixed

- `CITATION.cff` declared `license: Apache-2.0` while `LICENSE` is MIT; corrected to `license: MIT`.
- Added the missing `v0.17.0` changelog entry (release notes existed at `RELEASE_NOTES_v0.17.0.md` but were never reflected here).
- Removed a duplicated, out-of-order `## Unreleased` block that preceded the `# Changelog` heading.
- Refreshed `GITHUB_RELEASE_TEMPLATE.md`, which still referenced the v0.15.0 release.

## v0.17.0

- Completed the previously truncated MIT `LICENSE` file.
- Expanded CI to run the full documented validation gate: examples, feed descriptors, audit bundles, replay bundles, photography-contest walkthrough, conformance-pack export, release checksums, and tests.
- Added `CONTRIBUTING.md` with the release validation checklist and evidence expectations.
- Added `CODE_OF_CONDUCT.md`.
- Added minimal Docker packaging for the HTTP verifier service.
- Documented a GitHub Actions workflow for PyPI publication on GitHub Release publication (workflow file added in Unreleased above).
- Reframed documentation into role-based reading paths in the README.
- No schema, fixture, profile, conformance-matrix, or CLI behavior changes; downstream conformance consumers do not need to update fixtures or expected results.

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
