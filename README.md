# CAWG–TRQP Reference Implementation

**Version line:** post-v0.13.0 interoperability and documentation hardening  
**Status:** reference implementation with canonical fixture exchange, compatibility metadata, and HTTP integration coverage

## Overview

This repository shows how **TRQP** can serve as the governance decision plane in a **CAWG/C2PA** verification workflow.

The current state of the project goes beyond demonstrating a single verification loop. It now packages the repository as a reusable interoperability artifact. That means the code, fixtures, schemas, audit bundles, and compatibility signals are intended to travel together.

The result is a stronger handoff surface for developers, assurance teams, and governance programs that need more than a working demo. They need a verifier that can explain what it trusted, how it reached a decision, and how another implementation can reproduce the same outcome.

## What is now in place

### Deterministic input trust and replay fidelity

Profiles govern feed transport, revocation freshness, and replay evidence. The verifier records the transport posture and revocation status it relied on at decision time, and the audit bundle carries this forward as replayable evidence.

### Canonical fixture exchange for multiple deployment shapes

The repository now includes reusable profile-bound packages for:

- `standard-v1`
- `high-assurance-v1`
- `gateway-standard-v1`
- `multi-authority-v1`

These packages make the project usable as a conformance handoff artifact rather than only as source code.

### Machine-readable compatibility metadata

A compatibility matrix now lives under `conformance/compatibility-matrix.json`. It records which profiles, transport behaviors, revocation behaviors, and deployment surfaces are covered by the current repository state.

### HTTP deployment path coverage

The HTTP service is now documented and covered both through endpoint-level tests and a live-process integration test. This strengthens the claim that the repository is executable as a deployment reference, not only importable as a package.

### Documentation refresh

The documentation has been reviewed for freshness and expanded to explain the repository as an adoption surface, including fixture exchange, compatibility mapping, and the operational role of the HTTP service.

## Quick start

### Install

```bash
git clone <this-repo>
cd cawg-trqp-refimpl
pip install -r requirements-lock.txt
pip install -e .
```

### Run standard verification

```bash
python -m cawg_trqp_refimpl.cli       --fixture examples/fixtures/cawg_manifest_c2pa_pop.json       --profile standard
```

### Start the HTTP service

```bash
python scripts/start_http_service.py       --policy-path data/policies.json       --revocation-path data/revocations.json       --host 127.0.0.1       --port 5000
```

### Validate shipped artifacts

```bash
python scripts/validate_examples.py
pytest -q
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
```

## Canonical fixture packages

| Package | Verification mode | Primary use |
|---|---|---|
| `standard-v1` | `cached_online` | baseline exchange and replay |
| `high-assurance-v1` | `online_full` | strict live-only verification |
| `gateway-standard-v1` | `gateway_mediated` | mediated route evidence |
| `multi-authority-v1` | `gateway_mediated` | deterministic authority routing |

## Repository structure relevant to the current increment

- `fixtures/profile-bound/` — canonical fixture exchange packages for multiple deployment shapes
- `conformance/compatibility-matrix.json` — machine-readable compatibility declaration
- `docs/interoperability-vectors.md` — narrative guide to exchange artifacts
- `docs/compatibility-matrix.md` — explanation of the compatibility artifact
- `docs/http-transport-patterns.md` — deployment and testing guidance for the HTTP surface
- `tests/test_http_service_integration.py` — live-process HTTP test
- `requirements-lock.txt` — pinned validation dependency set used by CI

## Documentation map

- `docs/NON_TECHNICAL_OVERVIEW.md`
- `docs/architecture.md`
- `docs/INTEGRATION_GUIDE.md`
- `docs/interoperability-vectors.md`
- `docs/compatibility-matrix.md`
- `docs/http-transport-patterns.md`
- `docs/reproducibility-guide.md`
- `docs/trqp-alignment.md`
- `docs/verifier-profiles.md`
- `docs/release-readiness.md`
- `docs/repo-tree.md`

## Current roadmap direction

The earlier post-v0.13.0 fixture and compatibility goals are now substantially complete. The next practical increment should focus on stronger signed feed descriptors, richer freshness reason codes, and deeper integration hooks into external TRQP assurance suites.
