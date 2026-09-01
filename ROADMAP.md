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

## v0.17.0–v0.19.1 progression

Subsequent releases moved the repository from a broad executable verifier surface toward a more explicit adoption and assurance contract. The current repository includes executable adoption journeys, operator/public-safety assurance walkthroughs, machine-readable portfolio assurance evidence, scale/cache assurance guidance, and an explicit repository governance/status model.

The repository remains **pilot-ready**, not an independent certification service. CAWG/C2PA and TRQP normative authority remains upstream; this repository owns only its reference implementation behavior, repository-local profiles/fixtures, and generated assurance evidence.

## Current hardening tranche

The next advancement wave is intentionally falsification- and correctness-driven rather than another walkthrough expansion.

1. [#38 — isolate verifier evidence by decision](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/38): remove cross-decision evidence contamination risk from long-lived verifier instances.
2. [#39 — validate process evidence before verification](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/39): make malformed external evidence fail deterministically at the typed request boundary.
3. [#40 — make the repository completion gate authoritative](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/40): ensure local and CI assurance execute one machine-verifiable validation contract.
4. [#41 — expand adversarial verification vectors](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/41): add delegated-authority misuse, gateway substitution, revoked issuer, provenance stripping, and replay-root confusion vectors.

A patch release is appropriate once the correctness fixes, validation convergence, adversarial evidence, and roadmap/status evidence are complete and the authoritative repository gate passes.

## Deferred capability work

### Real binary CAWG/C2PA backend

Integrate a redistribution-safe binary C2PA parser behind `ManifestParserAdapter` only when deterministic fixture validation, dependency behavior, and licensing are settled. The adapter boundary is intentionally retained until those conditions can be evidenced.

### Production service packaging

Container/reverse-proxy examples, rate-limit policy, structured log routing, health/readiness probes, distributed cache adapters, single-flight refresh, and environment-specific load evidence remain deployment work. The repository should not convert benchmark contracts into fixed production throughput claims.

### Cross-repository alignment

Continue mapping assurance-suite, descriptor-policy, and adversarial-vector contracts into related TRQP conformance, assurance hub, TSPP, and trust infrastructure schema repositories where those repositories own the relevant contract surface.

## Completion rule

`make validate` is the repository-native completion gate. A roadmap item is not considered complete merely because documentation or code exists: its claimed behavior must have executable validation and reviewable evidence appropriate to the claim.
