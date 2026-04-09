# Changelog

## v0.12.0

### Added

- executable verification profile schema at `schemas/verification-profile.schema.json`
- built-in profiles at `profiles/edge.json`, `profiles/standard.json`, and `profiles/high_assurance.json`
- assurance overlays at `profiles/overlays/evidence_attested.json` and `profiles/overlays/freshness_strict.json`
- profile loader and overlay merge logic in `src/cawg_trqp_refimpl/profile.py`
- assurance-oriented profile tests in `tests/test_profiles.py`
- `RELEASE_NOTES_v0.12.0.md`

### Changed

- refactored verifier execution to resolve a machine-readable profile before making trust decisions
- enforced profile-aware fail-open and fail-closed behavior when live policy is unavailable
- embedded the resolved verification profile in `policy_evidence.verification_profile`
- exported the resolved verification profile object in `replay_inputs.profile`
- updated replay logic to consume embedded profile objects directly
- refreshed documentation to describe profile controls, overlays, and release validation
- bumped package version to `0.12.0`

### Assurance impact

This release turns verification profiles into executable governance artifacts. Verification output now captures not only a trust result, but the control semantics that produced it.

## v0.11.0

- add optional Ed25519 audit bundle attestation support
- verify bundle attestations against trust anchors during validation
- pin policy and revocation sources in replay_inputs.policy_feed
- allow replay tooling to resolve externalized policy feeds from bundle metadata
- add deterministic reproducibility fixture and comparison tooling
- refresh README, roadmap, release assets, release readiness, and architecture docs
- bump project version to 0.11.0
