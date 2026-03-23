# Suggested Release Assets

## Commit title

`release v0.7.0 with process-aware trust synthesis`

## Commit message

Release v0.7.0 with process-aware trust synthesis.

- add process_evidence request support and process_integrity result support
- enforce policy-level process requirements during trust synthesis
- parse process-oriented assertions from C2PA-style manifests
- refresh fixtures, schemas, README, architecture, roadmap, and release notes
- add Proof of Process reference path for future deeper integration

## Release title

`v0.7.0 – Process-Aware CAWG–TRQP Verification`

## Release summary

This release upgrades the CAWG–TRQP reference implementation from authorization-only decisioning to process-aware trust synthesis.

The verifier can now ingest process-oriented assertions, evaluate compact process evidence, and enforce policy requirements such as mandatory process proof, minimum confidence thresholds, and allowed process types. The result is a more realistic model of how CAWG/C2PA verification can incorporate Proof of Process style evidence without collapsing TRQP into an evidence-generation protocol.
