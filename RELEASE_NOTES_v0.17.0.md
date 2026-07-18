---
layout: default
title: "Release Notes v0.17.0"
parent: "Releases"
nav_order: 14
---
## v0.17.0 - Verified Quickstart & CI Parity

This adoption release closes the gap between the documented release gate and what CI actually enforces. It also fixes reuse blockers that would matter to downstream implementers, assurance teams, and security reviewers.

### Fixed

- Completed the previously truncated MIT `LICENSE` file.
- Expanded CI to run the full documented validation gate: examples, feed descriptors, audit bundles, replay bundles, photography-contest walkthrough, conformance-pack export, release checksums, and tests.

### Added

- `CONTRIBUTING.md` with the release validation checklist and evidence expectations.
- `CODE_OF_CONDUCT.md`.
- Minimal Docker packaging for the HTTP verifier service.
- GitHub Actions workflow for PyPI publication on GitHub Release publication.
- Role-based documentation reading paths in the README.

### Compatibility

No schema, fixture, profile, conformance-matrix, or CLI behavior changes are included. Downstream conformance consumers do not need to update fixtures or expected results.
