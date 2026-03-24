# CAWG–TRQP Reference Implementation

**Version:** v0.9.0  
**Status:** Reference implementation with signed offline snapshots, process-aware trust synthesis, exportable audit bundles, and trust gateway mediation

## Overview

This repository demonstrates how **TRQP** operates as the governance decision plane in a **CAWG/C2PA** verification workflow, and how that workflow can be extended with process-aware evidence, exportable audit bundles, and remote policy mediation.

By v0.9.0 the project covers the roadmap items for v0.8.0 and v0.9.0:

- exportable audit bundles that package verification result, policy evidence, and process appraisal together
- HTTP transport patterns for process-aware authorization and verification exchange
- benchmark fixtures for high-volume and constrained-device process-aware verification
- trust gateway component for remote policy mediation
- richer conformance and interoperability vectors
- deployment guidance for process-aware verifiers and appraisal services

## What v0.9.0 adds

### 1. Audit bundle export

The verifier can now package portable audit bundles that include:

- request summary
- verification result
- policy evidence
- process appraisal
- gateway mediation trace when enabled

### 2. Trust gateway mediation

A trust gateway component now models remote policy mediation. This lets deployments separate verification execution from policy routing while keeping a traceable mediation record.

### 3. HTTP transport patterns

The reference HTTP service now demonstrates:

- direct authorization lookup
- recognition lookup
- gateway-mediated authorization lookup
- end-to-end verification over HTTP
- audit bundle export over HTTP

### 4. Interoperability and benchmark fixtures

The repository now includes benchmark-style request fixtures for high-volume and constrained-device verification, along with gateway-oriented interoperability vectors.

### 5. Deployment guidance and executive framing

The docs now include:

- a deployment guide for process-aware verifiers and appraisal services
- a trust gateway architecture note
- an HTTP transport patterns note
- a non-technical overview for enterprise IT and business leaders

## Quick Start

### Install

```bash
git clone <this-repo>
cd cawg-trqp-verifier-refimpl
pip install -e .
```

### Run standard verification

```bash
python -m cawg_trqp_refimpl.cli --fixture examples/fixtures/cawg_manifest_c2pa_pop.json --profile standard
```

### Run gateway-mediated verification and export an audit bundle

```bash
python -m cawg_trqp_refimpl.cli   --fixture examples/fixtures/cawg_manifest_c2pa_pop.json   --profile standard   --use-gateway   --export-audit-bundle examples/exported_audit_bundle.json
```

### Start HTTP service

```bash
python scripts/start_http_service.py --port 5000
```

## Verification profiles

| Profile | Network posture | Policy source | Process posture | Primary use case |
|---|---|---|---|---|
| `edge` | intermittent or offline | signed snapshot only | local appraisal from supplied evidence | handheld, constrained, disconnected verification |
| `standard` | stable | cache-first with live lookup on miss | policy-aware composite decision | service and platform verification |
| `high_assurance` | stable | live lookup always | strict process policy enforcement | regulated or audit-sensitive verification |

## New components

### Audit bundle
Portable package that turns a verification event into a shareable evidence artifact.

### Trust gateway
Optional mediation layer for remote policy routing and governance traceability.

## Documentation map

- `docs/INTEGRATION_GUIDE.md`
- `docs/architecture.md`
- `docs/trust-gateway.md`
- `docs/http-transport-patterns.md`
- `docs/deployment-guide.md`
- `docs/NON_TECHNICAL_OVERVIEW.md`

## Roadmap status

The roadmap items through v0.9.0 are implemented in this release. The next step is to harden bundle formats and expand interoperability toward production-grade assurance exchange.
