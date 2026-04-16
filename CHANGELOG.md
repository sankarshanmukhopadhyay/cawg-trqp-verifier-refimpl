## Unreleased

- add canonical fixture packages for `high-assurance`, gateway-mediated, and multi-authority verification cases
- publish `conformance/compatibility-matrix.json` as a machine-readable adoption and assurance artifact
- add a live-process HTTP integration test to complement endpoint-level HTTP service coverage
- pin CI and validation dependencies in `requirements-lock.txt`
- refresh README and documentation to treat the repository as an external interoperability handoff surface

# Changelog

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
