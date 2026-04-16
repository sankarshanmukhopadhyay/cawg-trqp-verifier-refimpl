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
