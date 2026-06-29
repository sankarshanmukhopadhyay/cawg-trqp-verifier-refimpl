# GitHub Release Template

## Title

`v0.15.0 — Security Hardening and Roadmap Closure`

## Summary

This release hardens the CAWG-TRQP reference implementation across the API, profile, descriptor, and replay boundaries. It turns signed feed descriptors and replay evidence into stronger executable governance controls, especially for high-assurance verification.

## Highlights

- HTTP request hardening for content type, request size, typed fields, and safe profile resolution
- high-assurance fail-closed behavior for missing or invalid feed descriptor evidence
- robust descriptor validation for malformed descriptors, malformed timestamps, invalid base64, invalid signatures, digest mismatch, and unauthorized authorities
- audit replay hardening with trusted-root path boundaries and pinned digest validation
- updated compatibility matrix, roadmap, README, changelog, and release notes

## Validation

```bash
python scripts/validate_examples.py
python scripts/validate_feed_descriptors.py
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
pytest -q
```
