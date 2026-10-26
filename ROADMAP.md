---
layout: default
title: "Roadmap"
description: "Completed work, current release posture, and future work."
parent: "Governance & Policy"
nav_order: 5
---
# Roadmap

## Completed foundation through v0.16.0

v0.16.0 closed the practical roadmap items that were open after the v0.15.0 hardening release.

### External assurance-suite ingestion

- Added `conformance/assurance-suite-manifest.json` and `scripts/export_conformance_pack.py`.
- Mapped fixture packages to implementation identity, assurance level, vector class, replay contract, and evidence surfaces.
- Added machine validation with `python scripts/export_conformance_pack.py --check`.

### Binary CAWG/C2PA parser adapter boundary

- Added `src/cawg_trqp_refimpl/manifest_adapters.py`.
- Preserved JSON fixture and C2PA-style JSON envelope processing through `JsonManifestAdapter`.
- Reserved `C2PABinaryManifestAdapter` with deterministic unsupported-backend behavior.
- Documented the stable signal contract in `docs/parser-adapter-contract.md`.

### Descriptor policy and operational hardening

- Added `controls.descriptor_policy` with `observe`, `warn`, and `fail` semantics.
- Added structured HTTP audit events and operational deployment guidance.
- Added release checksum tooling and refreshed signed/replayable evidence artifacts.

## v0.17.0–v0.19.2 progression

Subsequent releases moved the repository from a broad executable verifier surface toward a more explicit adoption and assurance contract. The current repository includes executable adoption journeys, operator/public-safety assurance walkthroughs, machine-readable portfolio assurance evidence, scale/cache assurance guidance, and an explicit repository governance/status model.

The repository remains **pilot-ready**, not an independent certification service. CAWG/C2PA and TRQP normative authority remains upstream; this repository owns only its reference implementation behavior, repository-local profiles/fixtures, and generated assurance evidence.

## Completed v0.19.2 hardening tranche

The [v0.19.2 release](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/tag/v0.19.2) closes [#38](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/38), [#39](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/39), [#40](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/40) and [#41](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/41). All four are completed, not current work.

## Post-v0.19.2 experimental evidence gate

[Issue #75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75) tracks Delegated Creator feasibility and optional external C2PA validation. Independent C2PA/TRQP interoperability, identity/trust anchoring, signing-time assurance and actual delegated C2PA coverage remain **not demonstrated**. The next useful work is independently reproducible real-asset and trust-endpoint evidence, not further synthetic scenario expansion.

## Deferred capability work

### Real binary CAWG/C2PA backend

Integrate a redistribution-safe binary C2PA parser behind `ManifestParserAdapter` only when deterministic fixture validation, dependency behavior, and licensing are settled. The adapter boundary is intentionally retained until those conditions can be evidenced.

### Production service packaging

Container/reverse-proxy examples, rate-limit policy, structured log routing, health/readiness probes, distributed cache adapters, single-flight refresh, and environment-specific load evidence remain deployment work. The repository should not convert benchmark contracts into fixed production throughput claims.

### Cross-repository alignment

Continue mapping assurance-suite, descriptor-policy, and adversarial-vector contracts into related TRQP conformance, assurance hub, TSPP, and trust infrastructure schema repositories where those repositories own the relevant contract surface.

## Completion rule

`make validate` is the repository-native completion gate. A roadmap item is not considered complete merely because documentation or code exists: its claimed behavior must have executable validation and reviewable evidence appropriate to the claim.
