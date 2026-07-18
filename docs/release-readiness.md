---
layout: default
title: "Release Readiness"
description: "Whether repository artifacts are fit for external consumption."
parent: "Assurance & Evidence"
nav_order: 8
---
# Repository Readiness

This repository is no longer only organized around releases. It is also organized around whether its artifacts are fit for external consumption.

## Current readiness checklist

- [x] profiles and overlays are schema-driven and executable
- [x] descriptor enforcement policy is explicit by feed type
- [x] shipped examples and fixture packages validate against repository schemas
- [x] transport and revocation controls are exercised in positive and negative paths
- [x] canonical fixture exchange packages exist for multiple deployment shapes
- [x] a machine-readable compatibility matrix is published in the repository
- [x] an external assurance-suite manifest is published in the repository
- [x] the HTTP service surface is covered by both endpoint and live-process tests when Flask is installed
- [x] structured HTTP audit events are emitted for verification and audit-bundle operations
- [x] deterministic replay checks pass
- [x] signed audit bundle validation passes
- [x] release asset checksums are generated and checkable

## Validation commands

```bash
python scripts/validate_examples.py
pytest -q
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
python scripts/validate_feed_descriptors.py
python scripts/validate_photography_contest_example.py
python scripts/export_conformance_pack.py --check
python scripts/generate_release_checksums.py --check
```


## v0.16.0 readiness checklist

- [x] Snapshot evidence is current, signed, and descriptor digest validation passes.
- [x] Profile-bound fixture packages include current schema fields and expected results.
- [x] Reproducibility and photography contest replay bundles reproduce their expected results.
- [x] Descriptor policy is represented in profiles, schema, documentation, and runtime enforcement.
- [x] External assurance-suite manifest is generated and checkable.
- [x] Parser adapter contract is documented and importable.
- [x] HTTP verification and audit-bundle routes emit structured audit events.
- [x] Release checksums are generated and checkable.
- [x] Test suite passes with `68 passed`.


## v0.15.0 readiness checklist

- [x] HTTP service rejects non-JSON payloads, oversized requests, malformed verification requests, and unsafe profile path references.
- [x] API profile loading is restricted to built-in profiles and built-in overlay names.
- [x] High-assurance profile requires feed descriptor evidence and fails closed when descriptor evidence is missing or invalid.
- [x] Feed descriptor validation emits stable reason codes for malformed descriptors and malformed timestamps.
- [x] Audit bundle replay inputs can carry policy, revocation, descriptor, and trust-anchor source digests.
- [x] Replay checks bundle-referenced paths against a trusted root and verifies pinned digests before use.
- [x] Compatibility matrix declares v0.15.0 hardening controls and negative vectors.
- [x] Test coverage includes red-team regression cases in `tests/test_security_hardening.py`.


## v0.14.0 readiness checklist

- [x] Signed feed descriptor schema added.
- [x] Feed attestation schema added.
- [x] Policy, revocation, snapshot, and gateway route descriptor examples added.
- [x] Runtime verifier exports descriptor evidence under `policy_evidence.feed_descriptors`.
- [x] Audit bundle replay inputs carry descriptor evidence.
- [x] Negative descriptor vectors cover invalid signature, digest mismatch, unknown authority, and route attestation failure.
- [x] Validation script added: `python scripts/validate_feed_descriptors.py`.
- [x] Test suite command documented for CI and local validation.
