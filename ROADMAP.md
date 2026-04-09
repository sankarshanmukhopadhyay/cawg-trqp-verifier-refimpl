# Roadmap

## Current focus after v0.12.0

The repository now has an executable profile layer. The next increments should deepen transport, freshness, and cross-implementation assurance on top of that control plane.

### 1. Feed transport specialization

- add explicit HTTP / gateway / local transport controls to the profile model
- bind transport guarantees to replay evidence and validation expectations
- add transport-specific negative tests for partial policy availability

### 2. Revocation freshness assertions

- define freshness windows for revocation material
- surface freshness breach semantics in verification output and audit bundles
- add delta-channel fixtures and expiry-driven tests

### 3. Cross-implementation fixture exchange

- publish a fixture profile that packages request, resolved profile, expected result, and pinned feeds
- verify that replay results remain stable across independent implementations
- align fixture content with broader TRQP assurance and conformance work

## Completed in v0.12.0

- formalized verification profiles as schema-validated JSON artifacts
- introduced assurance overlays for tightening enforcement semantics without adding profile sprawl
- enforced fail-open and fail-closed behavior from profile controls
- embedded the resolved profile into audit bundles and replay workflows
- added profile tests covering overlay application and degraded-policy behavior

## Completed in v0.11.0

- added optional Ed25519 bundle attestation
- pinned external policy and revocation feeds in replay metadata
- added deterministic reproducibility fixtures and comparison tooling
