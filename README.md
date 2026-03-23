# CAWG–TRQP Reference Implementation

**Version:** v0.7.0  
**Status:** Reference implementation with signed offline snapshots, C2PA-style JSON manifest ingestion, and process-aware trust synthesis

## Overview

This repository demonstrates, in executable form, how **TRQP** operates as the **governance decision plane** in a **CAWG/C2PA** verification workflow and how that workflow can be upgraded with **Proof of Process** style evidence.

The architectural split is deliberate:

- **CAWG/C2PA** provides content-bound provenance and assertion packaging
- **Identity material** provides actor and issuer binding
- **TRQP** provides authorization and issuer-recognition answers
- **Process evidence** provides proof-oriented signals about how a content action was carried out
- **This verifier** synthesizes the final trust decision across online, cached, and offline modes

v0.7.0 jumps directly to the next substantive release line by adding a **process appraisal layer**, **policy-enforced process requirements**, and **process-aware fixtures, schemas, and examples**.

## What v0.7.0 Adds

### Process-aware verification

- `process_evidence` on verification requests
- `process_integrity` and `process_appraisal` on verification results
- Policy-level controls for:
  - `requires_process_proof`
  - `min_process_integrity`
  - `allowed_process_types`
- Composite trust synthesis that can reject otherwise authorized content when required process conditions are not met

### Proof of Process style integration path

- Parser support for process-oriented assertions in C2PA-style manifests
- Example fixtures carrying `cawg.process.proof` assertions
- Structured process appraisal aligned to a selective adoption model: TRQP remains the policy authority, while process evidence acts as an input to trust synthesis
- Repository references to the Proof of Process work for implementers exploring deeper attestation and appraisal patterns

### Documentation and packaging refresh

- Architecture, integration, implementation notes, verifier profiles, roadmap, and release-readiness docs refreshed
- Schemas updated for process-aware request and result objects
- Repo tree regenerated for new examples and release assets

## Quick Start

### Install

```bash
git clone <this-repo>
cd cawg-trqp-verifier-refimpl
pip install -e .
```

### Run standard verification

```bash
python -m cawg_trqp_refimpl.cli   --fixture examples/fixtures/cawg_manifest_c2pa_pop.json   --profile standard
```

### Run edge verification with signed snapshot

```bash
python -m cawg_trqp_refimpl.cli   --fixture examples/fixtures/cawg_manifest_c2pa_pop.json   --profile edge   --snapshot data/snapshot.json   --trust-anchors data/trust_anchors.json
```

### Start HTTP TRQP service

```bash
python scripts/start_http_service.py --port 5000
```

## Verification Profiles

| Profile | Network posture | Policy source | Process posture | Primary use case |
|---|---|---|---|---|
| `edge` | intermittent or offline | signed snapshot only | local appraisal from supplied evidence | handheld, constrained, disconnected verification |
| `standard` | stable | cache-first with live lookup on miss | policy-aware composite decision | service and platform verification |
| `high_assurance` | stable | live lookup always | strict process policy enforcement | regulated or audit-sensitive verification |

## Parser Modes

| Mode | Input shape | Purpose |
|---|---|---|
| `fixture` | simplified repo fixture | deterministic tests and quick demos |
| `c2pa_json` | C2PA-style manifest-store JSON | higher-fidelity CAWG/C2PA ingestion |

## Architecture

```text
CAWG/C2PA Manifest or Manifest Store
    ↓ extract actor, issuer, action, resource, assertions, provenance, process evidence
Identity Material
    ↓ bind issuer and actor context
TRQP Query Layer
    ↓ authorization + recognition + revocation signals + process requirements
Process Appraisal Layer
    ↓ evaluate supplied process evidence against policy thresholds
Verifier
    ↓ synthesize mode-specific trust decision
VerificationResult
```

For the edge profile, the policy path is:

```text
Signed Snapshot → Trust Anchor Verification → Freshness Check → Offline Authorization/Recognition → Process Appraisal → Trust Decision
```

## Example process-aware result fields

```json
{
  "actor_authorization": "authorized",
  "process_integrity": "verified_high",
  "trust_outcome": "trusted",
  "process_appraisal": {
    "status": "verified",
    "process_type": "human_assisted",
    "confidence": 0.92,
    "minimum_confidence": 0.75
  }
}
```

## Repository Structure

See `docs/repo-tree.md` for the refreshed tree and `docs/INTEGRATION_GUIDE.md` for the end-to-end workflow.

## Current Priorities

v0.7.0 closes a structural gap left open by earlier releases: the verifier can now express and enforce not only **who is allowed** to publish, but also **whether required process evidence accompanied the action**.

The next release track moves toward **transport realism, deployment hardening, and richer exportable audit bundles**.
