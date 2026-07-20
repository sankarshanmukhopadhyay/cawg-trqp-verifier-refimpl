# CAWG-TRQP Reference Implementation

> **Portfolio status:** Tier 1 flagship · Active · Beta

| Attribute | Value |
|---|---|
| Portfolio tier | Flagship |
| Lifecycle | Active |
| Primary role | reference verifier implementation |
| Primary output | Decision receipt and replayable audit bundle |
| Validation | `make validate` |
| Evidence output | See repository-specific output contract and examples |
| Governance authority | [`GOVERNANCE.md`](GOVERNANCE.md) |
| Stack adoption path | [`docs/trqp-adoption-path.md`](docs/trqp-adoption-path.md) |


**Version line:** v0.17.0 verified quickstart and CI parity  
**Status:** executable reference implementation with schema-backed profiles, signed feed descriptors, deterministic replay, fixture exchange, HTTP service hardening, external assurance-suite ingestion, and release-gated validation parity

## Overview

This repository shows how TRQP can operate as the governance decision plane for CAWG/C2PA-style content verification.

The verifier does more than return an allow or deny result. It records what authority was queried, which issuer was recognized, what process evidence was evaluated, which revocation posture was used, whether feed descriptors were valid, and whether the decision can be replayed from pinned inputs.

That makes the repository useful as:

- a developer reference implementation
- a conformance fixture source
- an assurance evidence model
- an HTTP deployment pattern
- a replayable governance decision example

## What v0.17.0 Adds

- Brings CI into parity with the documented release validation gate.
- Fixes the repository license grant so downstream reuse is legally inspectable.
- Adds contributor and conduct guidance for external implementers.
- Adds minimal Docker packaging for the HTTP verifier service.
- Adds release-triggered PyPI publishing workflow for package reuse.
- Reframes documentation into role-based reading paths for adoption.

## Quick Start

```bash
git clone <this-repo>
cd cawg-trqp-refimpl
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-lock.txt
pip install -e .
```

Run a standard verification:

```bash
python -m cawg_trqp_refimpl.cli examples/verification_request.json --profile standard
```

Run high-assurance verification with signed feed descriptors:

```bash
python -m cawg_trqp_refimpl.cli examples/verification_request.json \
  --profile high_assurance \
  --policy-descriptor examples/feed_descriptors/policy-feed.signed.json \
  --revocation-descriptor examples/feed_descriptors/revocation-feed.signed.json
```

Start the HTTP service:

```bash
python scripts/start_http_service.py \
  --policy-path data/policies.json \
  --revocation-path data/revocations.json \
  --host 127.0.0.1 \
  --port 5000
```

Run the HTTP service with Docker:

```bash
docker compose up --build
curl -sf http://127.0.0.1:5000/health
```

## Validation

Run the release validation gate:

```bash
python scripts/validate_api_contract.py
python scripts/validate_examples.py
python scripts/validate_feed_descriptors.py
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
python scripts/validate_photography_contest_example.py
python scripts/export_conformance_pack.py --check
python scripts/generate_release_checksums.py --check
pytest -q
```

Expected result for v0.17.0:

```text
70 passed
```

## Profiles

| Profile | Purpose | Descriptor posture |
|---|---|---|
| `standard` | Normal online or cached verification | Observe descriptor evidence |
| `high_assurance` | Live verification with fail-closed evidence requirements | Fail on policy, revocation, and gateway-route descriptor defects |
| `edge` | Offline snapshot verification | Fail on snapshot descriptor policy when configured |

Profiles are schema-backed by `schemas/verification-profile.schema.json`.

## Key Artifacts

| Path | Purpose |
|---|---|
| `src/cawg_trqp_refimpl/` | Verifier, service, replay, profile, descriptor, and parser code |
| `profiles/` | Built-in verification profiles and overlays |
| `schemas/` | JSON schemas for requests, results, profiles, receipts, descriptors, and audit bundles |
| `fixtures/profile-bound/` | Canonical fixture packages for external implementation comparison |
| `conformance/compatibility-matrix.json` | Machine-readable compatibility declaration |
| `conformance/assurance-suite-manifest.json` | External assurance-suite ingestion manifest |
| `examples/reproducibility_bundle_standard.json` | Canonical replay bundle |
| `examples/photography_contest/` | End-to-end contest verification walkthrough |
| `release-assets/checksums-v0.17.0.json` | Release asset checksum manifest |
| `assets/presentations/cawg-trqp-explainer-v2.pdf` | Non-normative explainer deck for standards and adoption review |
| `assets/presentations/manifest.json` | Presentation version, authority, checksum, and update triggers |

## Documentation

The full documentation set — all 30+ pages, organized by audience — is
published as a GitHub Pages site at
**https://sankarshanmukhopadhyay.github.io/cawg-trqp-verifier-refimpl/**,
built on the [Just the Docs](https://just-the-docs.com) theme with search.
The site is the recommended way to browse; the raw files below remain
authoritative and readable directly in the repository.

### New to this repository

- `docs/NON_TECHNICAL_OVERVIEW.md` — what this repository does, without assuming a technical background
- `docs/presentation.md` — presentation, slide-by-slide documentation map, embedded viewer, and maintenance policy
- `QUICKSTART.md` — first result in under ten minutes

### Implementers

- `docs/cawg-input-contract.md` — mandatory/optional CAWG signal mapping into TRQP verification requests
- `docs/api-call-catalogue.md` — complete implemented request/response and error surface
- `api/openapi.json` — machine-readable OpenAPI 3.1 contract
- `docs/INTEGRATION_GUIDE.md`
- `docs/verifier-profiles.md`
- `docs/descriptor-policy.md`
- `docs/feed-descriptor-profile.md`
- `docs/parser-adapter-contract.md`
- `docs/deterministic-input-trust.md`
- `docs/workflows/photography-contest-verification.md`
- `docs/video-verification-walkthrough.md`

### Integrators

- `docs/architecture.md`
- `docs/deployment-guide.md`
- `docs/http-transport-patterns.md`
- `docs/operational-hardening.md`
- `docs/trqp-alignment.md`
- `docs/trust-gateway.md`
- `docs/implementation-notes.md`

### Assurance Reviewers

- `docs/reproducibility-guide.md`
- `docs/audit-bundle-profile.md`
- `docs/assurance-suite-ingestion.md`
- `docs/compatibility-matrix.md`
- `docs/decision-receipt-specification.md`
- `docs/how-trqp-enables-assurance.md`
- `docs/risk-crosswalk.md`
- `docs/release-readiness.md`
- `docs/release-assets.md`

### Interoperability

- `docs/interoperability-vectors.md`
- `docs/trqp-adoption-path.md`

## Governance Model

The repository treats trust as executable governance:

- **Authority:** profile and policy feeds determine who can authorize or recognize.
- **Delegation:** gateway-mediated flows preserve route evidence and authority scope.
- **Enforcement:** revocation, descriptor policy, transport constraints, and process requirements affect outcomes.
- **Evidence:** decision results, decision receipts, audit bundles, replay bundles, and conformance manifests preserve auditability.
- **Revocation:** delta, live, and snapshot revocation postures are profile-controlled.
- **Replay:** pinned feeds and trusted replay roots make reliance decisions reproducible.

## Release Assets

Generate the external conformance manifest:

```bash
python scripts/export_conformance_pack.py
```

Generate release checksums:

```bash
python scripts/generate_release_checksums.py
```

The v0.17.0 release notes are in `RELEASE_NOTES_v0.17.0.md`.

## Responsible AI-assisted contribution

AI-assisted work is permitted only under accountable human review. See the [AI Usage Policy](AI_USAGE.md) and disclose material assistance in pull requests.
