# Release and Handoff Assets

Even when the repository is not being formally released, it still needs a disciplined handoff surface.

## Core handoff artifacts

- canonical fixture packages under `fixtures/profile-bound/`
- machine-readable compatibility matrix under `conformance/compatibility-matrix.json`
- reproducibility bundle under `examples/reproducibility_bundle_standard.json`
- signed and unsigned audit bundle examples under `examples/`

## Why these matter

Together, these files let another team evaluate the repository without first adopting the implementation. They can validate schemas, replay decisions, inspect transport and revocation evidence, and compare expected results against their own runtime.
