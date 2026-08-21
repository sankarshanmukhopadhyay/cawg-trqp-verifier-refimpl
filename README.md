# CAWG-TRQP Verifier Reference Implementation

> **Portfolio status:** Flagship · Pilot-ready · Active validation  
> **Current release:** v0.19.1  
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
| Cross-sector adoption | nineteen indexed sector walkthroughs, machine-readable scenarios, and three agentic assurance archetypes |
| Portfolio governance | repository-local status, governance, security, roadmap, release and integration evidence |

## What v0.19.1 adds

v0.19.1 is an assurance and portfolio-alignment patch. It does not change CAWG/C2PA verification semantics introduced in v0.19.0.

- Aligns machine-readable conformance and assurance manifests with the current release identity.
- Adds a machine-readable TRQP portfolio integration contract.
- Pins Trust Systems Meta-Model v0.24.0 as semantic authority and Trust Infrastructure Schemas v0.14.1 as schema/portfolio authority.
- Pins TRQP-TSPP v0.15.0, TRQP Conformance Suite v1.7.0, and TRQP Assurance Hub v1.10.0 as the synchronized TRQP release train consumed by this implementation.
- Declares explicit invalidation conditions for semantic/schema incompatibility, normative-source incompatibility, missing evidence, and release-identity mismatch.
- Adds CI validation for the portfolio integration contract and includes it in release checksum evidence.
- Retains the v0.19.0 semantic assurance controls for required CAWG/C2PA assertion labels, proposition-level evidence, deterministic conflict handling, degraded-state handling, and RAHP traceability.

Documentation on `main` may advance between releases where the change does not modify verifier semantics or the declared release contract. The walkthrough catalogue and operator guides are therefore treated as continuously maintainable adoption and assurance material.

## Start here

- [Guided learning paths](docs/guided-learning.md)
- [Non-technical overview](docs/NON_TECHNICAL_OVERVIEW.md)
- [Explainer presentation](docs/presentation.md) (17-slide orientation deck)
- [Quickstart](QUICKSTART.md)
- [Operator decision and replay walkthrough](docs/operator-decision-replay-walkthrough.md)
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

After the first verification, use the [operator walkthrough](docs/operator-decision-replay-walkthrough.md) to interpret the decision boundary, reason codes, evidence outputs, replay bundle, and correction lineage.

## Validation and assurance evidence

Run the complete repository gate:

```bash
make validate
```

The gate validates repository governance and documentation integrity, the OpenAPI contract, JSON examples, the v0.19.x semantic-assurance controls and walkthrough manifests, the TRQP portfolio integration contract, and the Python test suite. Release-specific checks remain available independently:

```bash
python scripts/validate_portfolio_contract.py
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

The repository now includes **nineteen indexed sector walkthroughs plus three agentic assurance archetypes**. The catalogue spans publication and public communication, rights and commercial authorization, regulated/evidentiary intake, field and operational evidence, long-lived correction-sensitive evidence, and constrained or humanitarian environments.

Recent assurance-boundary scenarios include disaster-response damage assessment, legal/administrative evidence submission, industrial inspection and maintenance evidence, cultural-heritage archive ingest, and official public-safety communications. The public-safety walkthrough is deliberately high-assurance: it separates authenticated media from the delegated authority to speak officially for an institution and pressure-tests incident scope, channel scope, revocation, stale trust state, conflict, correction, and agentic publishing.

Each indexed sector example defines a narrow decision boundary and makes revocation, stale state, authority conflict, correction, evidence outputs, and replay expectations explicit. See the [walkthrough catalogue](docs/sections/walkthroughs-index.md) for the current machine-linked portfolio rather than relying on release-era counts.

## Repository map

| Path | Purpose |
|---|---|
| `src/cawg_trqp_refimpl/` | verifier, HTTP service, parser, profiles, cache, and replay logic |
| `schemas/` | machine-readable requests, results, receipts, descriptors, profiles, and sector records |
| `profiles/` | standard, high-assurance, edge, and privacy overlays |
| `examples/` | canonical requests, receipts, audit bundles, and walkthrough scenarios |
| `fixtures/profile-bound/` | portable conformance fixture packages |
| `conformance/` | readiness matrices, compatibility declarations, and assurance manifests |
| `portfolio/` | machine-readable cross-repository integration contract |
| `docs/` | implementation, governance, adoption, privacy, risk, and operational guidance |
| `governance/` | machine-readable threat, abuse, processing, and residual-risk registers |
| `release-assets/` | release checksum evidence |

## Governance contract

- **Authority:** repository maintainers govern repository-local implementation, schemas, profiles, fixtures, and releases.
- **Delegation:** authority to approve changes is defined in [`GOVERNANCE.md`](GOVERNANCE.md).
- **Scope:** this project does not govern CAWG, C2PA, or TRQP specifications.
- **Enforcement:** CI, schema validation, conformance fixtures, revocation handling, portfolio-contract validation, and release checks operationalize the stated controls.
- **Revocation and supersession:** corrected results and releases create new evidence; historical receipts are not rewritten.
- **Auditability:** receipts, bundles, manifests, integration contracts, and checksums provide machine-verifiable evidence.

See [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml), [`SECURITY.md`](SECURITY.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and [`AI_USAGE.md`](AI_USAGE.md).

## Release

Release notes: [`RELEASE_NOTES_v0.19.1.md`](RELEASE_NOTES_v0.19.1.md)  
Changelog: [`CHANGELOG.md`](CHANGELOG.md)  
Roadmap: [`ROADMAP.md`](ROADMAP.md)

## License

MIT. See [`LICENSE`](LICENSE).

## Agentic AI assurance

The walkthrough portfolio includes a cross-cutting [Agentic AI Assurance](docs/agentic-ai/index.md) model that treats agents as delegated actors rather than trusted identities. It covers producer, submitter, verifier, orchestrator, proxy, and decision roles; binds actions to principals, mandates, scope, temporal validity, revocation, and replay evidence; and includes three executable archetypes under `examples/agent-*`.
