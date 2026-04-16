# v0.13.0 — Deterministic Input Trust and Replay Fidelity

This release makes the verifier more accountable about the information it trusts while producing a decision.

Earlier releases established executable profiles, assurance overlays, and replayable evidence. `v0.13.0` extends that work by treating transport posture, revocation freshness, and replay fidelity as first-class governance concerns.

## What is new

### Transport-aware profiles

Profiles can now declare what kind of feed path is acceptable and what integrity level that path must provide.

### Revocation freshness contracts

Profiles can now define how fresh revocation information must be, whether stale inputs should trigger warning or failure, and whether delta/live semantics are required.

### Richer replay evidence

Audit bundles now carry transport metadata, revocation status, and replay contract fields so downstream systems can inspect the input trust posture behind a decision.

### Canonical fixture package

The repository now includes a structured fixture package under `fixtures/profile-bound/standard-v1/` for cross-implementation replay and interoperability testing.

## Why it matters

A verification result is stronger when it can show not only what decision was reached, but also whether the policy and revocation inputs used for that decision met declared expectations.

That is the operational value of this release.
