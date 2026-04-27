# Repository Readiness

This repository is no longer only organized around releases. It is also organized around whether its artifacts are fit for external consumption.

## Current readiness checklist

- [x] profiles and overlays are schema-driven and executable
- [x] shipped examples and fixture packages validate against repository schemas
- [x] transport and revocation controls are exercised in positive and negative paths
- [x] canonical fixture exchange packages exist for multiple deployment shapes
- [x] a machine-readable compatibility matrix is published in the repository
- [x] the HTTP service surface is covered by both endpoint and live-process tests when Flask is installed
- [x] deterministic replay checks pass
- [x] signed audit bundle validation passes

## Validation commands

```bash
python scripts/validate_examples.py
pytest -q
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
```


## v0.14.0 readiness checklist

- [x] Signed feed descriptor schema added.
- [x] Feed attestation schema added.
- [x] Policy, revocation, snapshot, and gateway route descriptor examples added.
- [x] Runtime verifier exports descriptor evidence under `policy_evidence.feed_descriptors`.
- [x] Audit bundle replay inputs carry descriptor evidence.
- [x] Negative descriptor vectors cover invalid signature, digest mismatch, unknown authority, and route attestation failure.
- [x] Validation script added: `python scripts/validate_feed_descriptors.py`.
- [x] Test suite passes: `52 passed, 6 skipped`.
