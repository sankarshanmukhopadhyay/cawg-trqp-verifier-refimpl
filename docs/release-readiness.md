# Release Readiness

## v0.13.0 checklist

- [x] transport controls added to profile schema
- [x] revocation freshness controls added to profile schema
- [x] verifier enforces transport and freshness guardrails
- [x] audit bundles carry replay fidelity extensions
- [x] canonical fixture package added
- [x] example bundles rebuilt
- [x] documentation refreshed
- [x] test suite passes

## Validation commands

```bash
pytest -q
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
```
