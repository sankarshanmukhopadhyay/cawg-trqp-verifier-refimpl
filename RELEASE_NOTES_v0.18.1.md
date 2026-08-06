# CAWG-TRQP Verifier Reference Implementation v0.18.1

## Release purpose

v0.18.1 broadens the repository from a small set of content-industry examples into a cross-sector executable-governance walkthrough portfolio while closing portfolio-governance and documentation-validation findings.

## Added

- Ten publication-ready real-life walkthroughs with matching machine-readable scenario manifests.
- Automated validation for required cases: authorized, scope mismatch, revoked, stale, conflicting, and corrected.
- `PROJECT-STATUS.yaml` aligned to the portfolio member status schema and CAWG-TRQP authority boundaries.

## Fixed

- Removed unresolved `Documentation` navigation parents from guided-learning and documentation-architecture pages.
- Added repository validation to CI so Pages navigation failures are caught on every supported Python version.
- Refreshed the README to reflect current capabilities, evidence outputs, walkthrough coverage, limitations, and release posture.

## Governance and assurance

The release makes authority ownership, non-asserted claims, delegation, supersession, validation commands, evidence outputs, and known limitations machine-readable. The new walkthroughs consistently distinguish provenance and authorization evidence from truth or domain-professional judgment.

## Validation

```bash
make validate
python scripts/validate_feed_descriptors.py
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
python scripts/export_conformance_pack.py --check
python scripts/generate_release_checksums.py --check
```

## Compatibility

No intentional breaking API or schema change. Existing verifier profiles and established walkthroughs remain supported.
