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

The latest published release is [v0.19.2](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/tag/v0.19.2), whose wheel, source archive and checksum evidence are attached to GitHub Releases. Current `main` may contain later experimental work; resolve reproducible release evidence at the release tag rather than treating `main` as an immutable release.

## Core handoff artifacts

- canonical fixture packages under `fixtures/profile-bound/`
- machine-readable compatibility matrix under `conformance/compatibility-matrix.json`
- reproducibility bundle under `examples/reproducibility_bundle_standard.json`
- signed and unsigned audit bundle examples under `examples/`

## Why these matter

Together, these files let another team evaluate the repository without first adopting the implementation. They can validate schemas, replay decisions, inspect transport and revocation evidence, and compare expected results against their own runtime.
