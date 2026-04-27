# v0.14.0 — Signed Feed Descriptors and Runtime Evidence Hardening

This release moves the reference implementation from recording policy inputs to proving the authority, integrity, freshness, and route posture of the feeds used by the verifier.

## Highlights

- Adds signed feed descriptor schemas for policy, revocation, snapshot, and gateway-mediated feed routes.
- Adds runtime descriptor validation and exports descriptor evidence into verification results.
- Carries feed descriptor evidence into audit bundle replay inputs.
- Normalizes freshness and descriptor failures through stable reason codes.
- Adds negative conformance tests for digest mismatch, invalid signature, unknown authority, and unattested route conditions.
- Adds an adoption-oriented feed descriptor profile document and validation script.

## Validation

Validated with:

```bash
pytest -q
python scripts/validate_feed_descriptors.py
python scripts/validate_examples.py
```

Current test posture: `52 passed, 6 skipped`.

## Migration note

Existing verifier usage remains compatible. Feed descriptor enforcement activates when descriptor paths are supplied to `MockTRQPService`. Integrators can adopt this increment incrementally by first validating descriptors and observing reason codes before making descriptor failures fail-closed in deployment policy.
