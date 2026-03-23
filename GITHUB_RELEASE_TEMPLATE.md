# GitHub Release Template

## Commit Title
```
release v0.7.0 with process-aware trust synthesis
```

## Commit Message
```
Release v0.7.0 with process-aware trust synthesis

This release upgrades the CAWG–TRQP reference implementation from
authorization-only decisioning to process-aware trust synthesis.

## Major Additions

### Process-aware verification
- add process_evidence support on VerificationRequest
- add process_integrity and process_appraisal on VerificationResult
- add verifier-side appraisal logic that can reject otherwise authorized content
  when required process conditions are not met

### Policy requirements for process proof
- allow authorization entries to carry requires_process_proof,
  min_process_integrity, and allowed_process_types
- enforce those requirements in online and offline verification flows
- keep TRQP as policy authority while process evidence remains an input

### C2PA parser extension
- parse process-oriented assertions such as cawg.process.proof
- add process-aware C2PA fixtures and update example bundles
- preserve backward compatibility with simplified fixtures

### Documentation refresh
- update README, roadmap, architecture, implementation notes,
  verifier profiles, integration guide, release readiness, and repo tree
- add release notes for v0.7.0
- include reference path to LF Decentralized Trust Labs Proof of Process repo

## Testing
- expand verifier tests for successful and failed process-aware verification
- preserve existing cache, snapshot, parser, and HTTP service coverage
```

## GitHub Release Notes

### Release Title
```
v0.7.0 – Process-Aware CAWG–TRQP Verification
```

### Release Body

```markdown
## Overview

This release upgrades the CAWG–TRQP reference implementation from authorization-only decisioning to process-aware trust synthesis.

The verifier can now ingest process-oriented assertions, evaluate compact process evidence, and enforce policy requirements such as mandatory process proof, minimum confidence thresholds, and allowed process types.

## What is new

### Process-aware verification
- `process_evidence` added to verification requests
- `process_integrity` and `process_appraisal` added to verification results
- trust outcomes can now be rejected when authorization passes but required process conditions are not met

### Policy and parser upgrades
- authorization policy entries can now express process requirements
- parser supports process-oriented assertions in C2PA-style manifest-store JSON
- new fixtures demonstrate successful and failed process-proof paths

### Documentation refresh
- README and integration docs now explain the governance plane plus process plane split
- schemas, examples, roadmap, and release readiness updated for v0.7.0

## Why this matters

TRQP answers whether a publishing action is authorized. Process evidence adds a way to model whether the action was carried out under the kind of process policy expects. Together they produce a more realistic trust decision.

## Reference path

This repository includes a selective integration path for ideas from LF Decentralized Trust Labs Proof of Process work and points implementers to that repository for deeper evidence and appraisal models.

## Testing

Run:

```bash
pytest tests/ -v
```

See `RELEASE_NOTES_v0.7.0.md` for the detailed release summary.
```
