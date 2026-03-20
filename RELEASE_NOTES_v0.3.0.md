# Release Notes: v0.3.0

This release moves the CAWG–TRQP reference implementation from a basic executable skeleton to a more repo-ready engineering artifact.

## Highlights

- Added simplified CAWG/C2PA fixture handling to make verification flows more concrete.
- Added release-readiness documentation and issue-ready gap notes.
- Added GitHub Actions CI workflow for tests.
- Added revocation data source and expected result fixtures.
- Improved repository structure for easier GitHub publication.

## Why this matters

The repo now does a better job of showing where TRQP sits in the architecture:

- **CAWG/C2PA fixture layer** provides content-bound evidence input.
- **Verifier** validates integrity and extracts identifiers.
- **TRQP service / snapshot** provides authorization and recognition answers.
- **Decision engine** synthesizes the final result.

That makes the governance-plane role of TRQP operationally visible.
