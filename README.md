# CAWG-TRQP Verifier Reference Implementation

> **Portfolio status:** Flagship · Pilot-ready · Active validation  
> **Current release:** v0.18.1  
> **Project status declaration:** [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml)

| Portfolio tier | Flagship |
| Validation | `make validate` |
| Evidence output | decision receipts, audit bundles, replay bundles, conformance manifests |
| Governance authority | [`GOVERNANCE.md`](GOVERNANCE.md) and [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml) |

This repository is an executable reference implementation for applying **Trust Registry Query Protocol (TRQP)** governance decisions to **CAWG/C2PA-style content-authenticity evidence**. It converts validated provenance signals into scoped, replayable decisions about whether an actor may perform a specific action on a specific resource under a recorded policy and trust state.

It does **not** treat provenance as truth, ownership, entitlement, clinical validity, or professional judgment. Those responsibilities remain with the relying organization.

## Current capability

| Capability | Repository evidence |
|---|---|
| Authority and recognition | policy feeds, trust anchors, recognition responses |
| Delegation and action scope | authorization requests, gateway routes, context profiles |
| Enforcement and revocation | live, delta, snapshot, and fail-closed descriptor policies |
| Auditability | stable reason codes, decision receipts, signed audit bundles |
| Reproducibility | pinned replay bundles and trusted replay roots |
| Privacy controls | minimization, retention, redaction, and rights profiles |
| Cross-sector adoption | fourteen end-to-end walkthroughs and machine-readable examples |
| Portfolio governance | repository-local status, governance, security, roadmap, and release evidence |

## What v0.18.1 adds

- Ten real-life governance walkthroughs spanning journalism, insurance, marketplaces, healthcare, public evidence, construction, humanitarian response, political advertising, warranties, and research imagery.
- Machine-readable scenario manifests covering authorization, scope mismatch, revocation, stale trust state, authority conflict, and correction.
- `PROJECT-STATUS.yaml`, closing the portfolio-governance status-declaration finding.
- Corrected GitHub Pages navigation-parent declarations that previously failed the flagship repository validation gate.
- A refreshed README aligned with the current implementation, evidence model, validation commands, and limitations.

## Start here

- [Guided learning paths](docs/guided-learning.md)
- [Non-technical overview](docs/NON_TECHNICAL_OVERVIEW.md)
- [Quickstart](QUICKSTART.md)
- [Walkthrough catalogue](docs/sections/walkthroughs-index.md)
- [Documentation site](https://sankarshanmukhopadhyay.github.io/cawg-trqp-verifier-refimpl/)

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-lock.txt
pip install -e .
python -m cawg_trqp_refimpl.cli examples/verification_request.json --profile standard
```

Start the HTTP service:

```bash
python scripts/start_http_service.py \
  --policy-path data/policies.json \
  --revocation-path data/revocations.json \
  --host 127.0.0.1 --port 5000
```

## Validation and assurance evidence

Run the complete repository gate:

```bash
make validate
```

The gate validates repository governance and documentation integrity, the OpenAPI contract, JSON examples, the v0.18.1 walkthrough manifests, and the Python test suite. Release-specific checks remain available independently:

```bash
python scripts/validate_feed_descriptors.py
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
python scripts/export_conformance_pack.py --check
python scripts/generate_release_checksums.py --check
```

## Verification profiles

| Profile | Intended use | Failure posture |
|---|---|---|
| `standard` | Online or cache-assisted verification | records descriptor evidence and policy state |
| `high_assurance` | Consequential decisions requiring current governed evidence | fails closed on required descriptor defects |
| `edge` | Offline or intermittently connected operation | uses governed snapshots and exposes staleness |

Profiles are schema-backed by [`schemas/verification-profile.schema.json`](schemas/verification-profile.schema.json).

## Walkthrough portfolio

The repository now includes fourteen end-to-end examples. Established examples cover photography contests, operational video, authorized music distribution, and AI-assisted property listings. The v0.18.1 portfolio adds:

- breaking-news photography;
- insurance claim evidence;
- marketplace product images;
- medical imaging for remote consultation;
- body-camera and municipal evidence;
- construction milestone certification;
- humanitarian offline field evidence;
- political campaign advertising;
- warranty and repair evidence; and
- scientific research imagery.

Each new example defines a narrow decision boundary and tests revocation, stale state, authority conflict, correction, and immutable evidence lineage.

## Repository map

| Path | Purpose |
|---|---|
| `src/cawg_trqp_refimpl/` | verifier, HTTP service, parser, profiles, cache, and replay logic |
| `schemas/` | machine-readable requests, results, receipts, descriptors, profiles, and sector records |
| `profiles/` | standard, high-assurance, edge, and privacy overlays |
| `examples/` | canonical requests, receipts, audit bundles, and walkthrough scenarios |
| `fixtures/profile-bound/` | portable conformance fixture packages |
| `conformance/` | readiness matrices, compatibility declarations, and assurance manifests |
| `docs/` | implementation, governance, adoption, privacy, risk, and operational guidance |
| `governance/` | machine-readable threat, abuse, processing, and residual-risk registers |
| `release-assets/` | release checksum evidence |

## Governance contract

- **Authority:** repository maintainers govern repository-local implementation, schemas, profiles, fixtures, and releases.
- **Delegation:** authority to approve changes is defined in [`GOVERNANCE.md`](GOVERNANCE.md).
- **Scope:** this project does not govern CAWG, C2PA, or TRQP specifications.
- **Enforcement:** CI, schema validation, conformance fixtures, revocation handling, and release checks operationalize the stated controls.
- **Revocation and supersession:** corrected results and releases create new evidence; historical receipts are not rewritten.
- **Auditability:** receipts, bundles, manifests, and checksums provide machine-verifiable evidence.

See [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml), [`SECURITY.md`](SECURITY.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and [`AI_USAGE.md`](AI_USAGE.md).

## Release

Release notes: [`RELEASE_NOTES_v0.18.1.md`](RELEASE_NOTES_v0.18.1.md)  
Changelog: [`CHANGELOG.md`](CHANGELOG.md)  
Roadmap: [`ROADMAP.md`](ROADMAP.md)

## License

MIT. See [`LICENSE`](LICENSE).

## Agentic AI assurance

The walkthrough portfolio includes a cross-cutting [Agentic AI Assurance](docs/agentic-ai/index.md) model that treats agents as delegated actors rather than trusted identities. It covers producer, submitter, verifier, orchestrator, proxy, and decision roles; binds actions to principals, mandates, scope, temporal validity, revocation, and replay evidence; and includes three executable archetypes under `examples/agent-*`.

