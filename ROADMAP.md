---
layout: default
title: "Roadmap"
description: "Completed work, current release posture, and future work."
parent: "Governance & Policy"
nav_order: 5
---
# Roadmap

## Completed Through v0.16.0

v0.16.0 closes the practical roadmap items that were open after the v0.15.0 hardening release.

### External Assurance-Suite Ingestion

- Added `conformance/assurance-suite-manifest.json`.
- Added `scripts/export_conformance_pack.py`.
- Mapped fixture packages to implementation identity, assurance level, vector class, replay contract, and evidence surfaces.
- Added validation support with `python scripts/export_conformance_pack.py --check`.

### Binary CAWG/C2PA Parser Adapter Boundary

- Added `src/cawg_trqp_refimpl/manifest_adapters.py`.
- Preserved the JSON fixture and C2PA-style JSON envelope path through `JsonManifestAdapter`.
- Added a reserved `C2PABinaryManifestAdapter` boundary with deterministic unsupported-backend behavior.
- Documented the stable signal contract in `docs/parser-adapter-contract.md`.

### Descriptor Policy Configuration

- Added `controls.descriptor_policy` to verification profiles.
- Added `observe`, `warn`, and `fail` semantics for policy, revocation, snapshot, and gateway-route descriptors.
- Updated built-in profiles and schema validation.
- Documented policy behavior in `docs/descriptor-policy.md`.

### Operational Hardening

- Added structured HTTP audit events for verification and audit-bundle routes.
- Added deployment guidance in `docs/operational-hardening.md`.
- Added release checksum tooling and `release-assets/checksums-v0.16.0.json`.
- Refreshed release validation commands and readiness checks.

### Evidence and Artifact Refresh

- Refreshed signed snapshot evidence.
- Regenerated profile-bound fixtures and expected results.
- Regenerated reproducibility and audit-bundle examples.
- Regenerated photography contest replay evidence.
- Restored a passing validation posture across scripts and tests.

## Current Release Posture

The repository is an executable CAWG-TRQP assurance surface. It supports:

- schema-backed verification profiles
- signed feed descriptors
- deterministic replay bundles
- canonical fixture exchange
- HTTP service hardening
- structured audit events
- external assurance-suite ingestion
- release asset checksums

## Future Work

### 1. Real Binary CAWG/C2PA Backend

Integrate a redistribution-safe binary C2PA parser behind `ManifestParserAdapter` when deterministic fixture validation and dependency licensing are settled.

### 2. Expanded Negative Vector Library

Add more adversarial fixtures for delegated authority misuse, gateway route substitution, revoked issuer recognition, partial provenance stripping, and replay-root confusion.

### 3. Production Service Packaging

Add a containerized deployment profile with reverse-proxy examples, rate-limit policy, structured log routing, and health/readiness probes.

### 4. Cross-Repository Alignment

Map the assurance-suite manifest and descriptor policy controls into related TRQP conformance, assurance hub, TSPP, and trust infrastructure schema repositories.

## Scale and cache assurance

The reference implementation now provides persistent HTTP cache semantics, replaceable cache interfaces, scale architecture guidance and reproducible benchmark contracts. Production-grade distributed cache adapters, single-flight refresh and environment-specific load evidence remain deployment work rather than fixed throughput claims.
