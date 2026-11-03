---
layout: default
title: "Release & Handoff Assets"
description: "The disciplined handoff surface maintained independent of formal releases."
parent: "Assurance & Evidence"
nav_order: 9
---
# Release and Handoff Assets

Even when the repository is not being formally released, it still needs a disciplined handoff surface.

## Published release versus current branch

The current release baseline is [v0.20.0](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/tag/v0.20.0). Source distribution, wheel, and the checksum evidence manifest for selected machine-readable artifacts are attached to GitHub Releases. The Delegated Creator and external C2PA work is experimental, not independently interoperable. Pin the release tag to reproduce the evidence; `main` may move after publication.

## Checksum reproduction

From a clean checkout of the release tag, first run `make validate`, then:

```bash
python scripts/generate_release_checksums.py
python scripts/generate_release_checksums.py --check
```

Compare the generated manifest to the
[v0.20.0 checksum attachment](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/download/v0.20.0/checksums-v0.20.0.json)
when auditing the *tagged* evidence. The attachment lists SHA-256 digests
of selected conformance, portfolio and replay inputs; it is not a signed
attestation or a digest list for the wheel and source distribution.

## Core handoff artifacts

- canonical fixture packages under `fixtures/profile-bound/`
- machine-readable compatibility matrix under `conformance/compatibility-matrix.json`
- reproducibility bundle under `examples/reproducibility_bundle_standard.json`
- signed and unsigned audit bundle examples under `examples/`

## Why these matter

Together, these files let another team evaluate the repository without first adopting the implementation. They can validate schemas, replay decisions, inspect transport and revocation evidence, and compare expected results against their own runtime.
