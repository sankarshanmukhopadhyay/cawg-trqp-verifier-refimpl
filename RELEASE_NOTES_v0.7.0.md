# v0.7.0 – Process-Aware CAWG–TRQP Verification

## Overview

This release upgrades the CAWG–TRQP reference implementation from authorization-only decisioning to process-aware trust synthesis.

The key design move is straightforward: TRQP remains the policy authority, while process evidence becomes an additional input that can strengthen or block a trust decision depending on the policy requirements attached to the authorization path.

## What changed

### 1. Process-aware verification model
- Added `process_evidence` to verification requests
- Added `process_integrity` and `process_appraisal` to verification results
- Added verifier-side appraisal logic for compact process evidence
- Added explicit failure paths for missing required proof, insufficient confidence, and failed verification

### 2. Policy upgrades
- Added `policy_requirements` to authorization records
- Added support for `requires_process_proof`
- Added support for `min_process_integrity`
- Added support for `allowed_process_types`
- Applied the same logic in online and snapshot-backed edge verification

### 3. Parser and example refresh
- Extended C2PA-style parser path to extract process-oriented assertions
- Added `examples/fixtures/cawg_manifest_c2pa_pop.json`
- Added `examples/fixtures/cawg_manifest_c2pa_pop_failed.json`
- Updated expected results and example request payloads

### 4. Documentation refresh
- Updated README, roadmap, integration guide, architecture, implementation notes, verifier profiles, release-readiness, and repo tree
- Added explicit reference path to the Proof of Process repository for implementers who want deeper evidence packet and appraisal models

## Practical impact

This repository now models a more realistic trust decision:

- **authorization** still answers whether the actor is allowed to perform the action
- **recognition** still answers whether the issuer is recognized
- **process appraisal** now answers whether the supplied process evidence satisfies the policy conditions for a trusted outcome

That shift makes the verifier materially more useful for editorial, media, and other provenance-sensitive workflows where policy is not only about identity and authorization, but also about how the action was carried out.

## Next

The next release focus is v0.8.0:

- exportable audit bundles
- transport patterns for process-aware exchange
- benchmark fixtures for constrained and high-volume verification paths
