# Changelog

All notable changes to the CAWG–TRQP reference implementation are documented here.

## [v0.7.0] – 2026-03-23

### Added

#### Process-aware trust synthesis
- `process_evidence` on verification requests
- `process_integrity` and `process_appraisal` on verification results
- process appraisal logic in the verifier
- policy-level process requirements on authorization entries
- process-aware examples and expected results

#### Proof of Process style integration path
- parser support for process-oriented assertions in C2PA-style manifests
- new fixtures: `cawg_manifest_c2pa_pop.json` and `cawg_manifest_c2pa_pop_failed.json`
- compact reference path to the Proof of Process repository for deeper evidence and appraisal modeling

### Changed
- version bump to `0.7.0`
- README, roadmap, integration guide, architecture, implementation notes, verifier profiles, and release-readiness docs refreshed
- schemas updated for process-aware request and result shapes
- policy and snapshot examples now carry process requirements

## [v0.5.0] – 2026-03-23

### Added

#### Signed snapshot verification (Issue #002)
- Ed25519 signature verification for `data/snapshot.json`
- Trust-anchor store in `data/trust_anchors.json`
- Snapshot expiry enforcement via `expires_at`
- Failure states for missing signature, invalid signature, unknown signer, and expired snapshot
- `scripts/sign_snapshot.py` for deterministic snapshot signing

#### Real C2PA-style JSON parser path (Issue #001)
- Parser support for `manifest_store` envelopes and active manifest selection
- Extraction of actor, issuer, credential type, action, resource, assertions, and provenance chain
- New realistic fixture: `examples/fixtures/cawg_manifest_c2pa.json`
- `fixture_loader.py` now builds verification requests from parser output instead of fixture-specific field assumptions

#### Delivery and test hardening
- Snapshot signature tamper and expiry tests
- Parser-mode validation for C2PA-style inputs
- `pytest` source-path configuration in `pyproject.toml`
- `cryptography` dependency added for Ed25519 verification

### Changed
- Version bump to `0.5.0`
- Edge verification now rejects unusable snapshots instead of silently trusting unsigned snapshot state
- `examples/fixtures/content_bundle_example.json` now points to the C2PA-style fixture path
- README and integration documentation updated for signed offline verification

## [v0.4.0] – 2026-03-20

### Added
- HTTP TRQP service
- CAWG/C2PA manifest parser with simplified fixtures and fallback logic
- Revocation delta handling
- Expanded conformance suite
- Comprehensive documentation refresh

## [v0.3.1] – 2026-03-20

### Added
- Explicit release-readiness assessment
- v0.3.1 release notes

### Changed
- Tightened public-facing README
- Refreshed repository tree documentation

## [v0.3.0] – 2026-03-19

### Added
- Release-readiness documentation
- Simplified CAWG/C2PA fixture ingestion
- Revocation data source
- GitHub Actions CI workflow
- Roadmap and issue-ready gap log
- Expected result fixtures
- Improved repository structure for public release

## [v0.2.0] – 2026-03-18

### Added
- Executable reference implementation skeleton
- Mock TRQP service with policy and recognition queries
- TTL cache and snapshot loader
- Command-line interface
- Unit tests and demo runner
- Three verification profiles: edge, standard, high_assurance
