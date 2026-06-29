# Release Notes: v0.15.0

## Security Hardening and Roadmap Closure

v0.15.0 is a security and assurance release for the CAWG-TRQP reference implementation. It hardens the trust boundaries that matter most for a verifier: API request handling, profile authority, signed feed descriptor enforcement, replay input integrity, and release metadata consistency.

The release also closes the prior roadmap items around signed feed descriptors, richer freshness reason codes, and runtime evidence export. The remaining roadmap is now narrowed to external conformance-suite ingestion, a binary CAWG/C2PA parser adapter, descriptor policy configuration, and operational deployment hardening.

## What Changed

### HTTP Boundary Hardening

- The Flask service now enforces `application/json` request bodies.
- Request bodies are bounded with a maximum content length.
- Verification request fields are validated for required presence and expected types.
- API callers can select built-in profiles and overlays, but cannot resolve arbitrary local profile files through the HTTP boundary.
- Audit-bundle profile errors are returned as structured `invalid_request` responses instead of server exceptions.

### Profile Authority and High-Assurance Enforcement

- Added safe API profile loading through `load_api_profile`.
- Added `evidence.require_feed_descriptors` to the verification profile schema.
- The `high_assurance` profile now requires policy and revocation feed descriptor evidence.
- Missing or invalid required descriptor evidence causes fail-closed behavior through the existing transport/revocation guardrail path.

### Feed Descriptor Robustness

- Descriptor validation now handles malformed descriptors, malformed timestamps, invalid base64 signatures, and invalid Ed25519 signature lengths as stable evidence conditions.
- Added the `descriptor_malformed` reason code.
- Descriptor failures now remain machine-readable through `policy_evidence.feed_descriptors`.

### Audit Replay Integrity

- Audit bundles can now preserve source paths and digests for policy, revocation, descriptor, and trust-anchor inputs.
- Replay checks bundle-referenced files against a trusted replay root before loading them.
- Replay validates pinned digests before referenced feeds can influence the replay result.
- `scripts/replay_audit_bundle.py` now accepts `--trusted-root`.

### Conformance and Documentation

- Added `tests/test_security_hardening.py` for red-team regression coverage.
- Updated `conformance/compatibility-matrix.json` with v0.15.0 security controls and negative vectors.
- Updated `ROADMAP.md` to mark prior work as complete and define the next practical increments.
- Updated README, changelog, release-readiness notes, and version metadata.

## Security Impact

This release reduces ambient trust in three places:

1. API callers no longer control filesystem profile resolution.
2. Audit replay no longer accepts bundle-referenced files without path-boundary and digest checks.
3. High-assurance verification no longer treats missing descriptor evidence as merely informational.

The implementation remains a reference implementation, not a production web service distribution. Production deployments should still place the Flask service behind a real reverse proxy, TLS termination, request-rate controls, structured logging, and deployment-specific authorization.

## Validation

Run:

```bash
pip install -r requirements-lock.txt
pip install -e .
python scripts/validate_examples.py
python scripts/validate_feed_descriptors.py
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
pytest -q
```

## Compatibility Notes

- Standard profile behavior remains observational for descriptor evidence.
- High-assurance profile behavior is stricter: required feed descriptors must be present and valid.
- HTTP callers that previously supplied filesystem paths as `profile` values must now use built-in profile names or inline profile objects.
- Replay callers using bundle-provided file paths must ensure those paths resolve under the selected trusted root.

## Key Files

- `src/cawg_trqp_refimpl/http_service.py`
- `src/cawg_trqp_refimpl/profile.py`
- `src/cawg_trqp_refimpl/feed_descriptor.py`
- `src/cawg_trqp_refimpl/verifier.py`
- `src/cawg_trqp_refimpl/audit.py`
- `src/cawg_trqp_refimpl/replay.py`
- `schemas/verification-profile.schema.json`
- `tests/test_security_hardening.py`
- `conformance/compatibility-matrix.json`
- `ROADMAP.md`
