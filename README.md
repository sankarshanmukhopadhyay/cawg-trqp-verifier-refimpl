# CAWG-TRQP Verifier Reference Implementation

> **Portfolio status:** Flagship · Pilot-ready · Active validation  
> **Latest published release:** v0.21.0 · **`main`:** post-v0.21.0 development (release tag is the reproducible baseline)  
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
| Executable adoption | HTTP-to-audit-bundle and operational failure/redress journeys with CI-validated journey contracts |
| Portfolio governance | repository-local status, governance, security, roadmap, release and integration evidence |

## Published release and current development

The [v0.21.0 experimental consent-evidence release](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/tag/v0.21.0) adds independent *claimed* consent assessment and two synthetic cross-taskforce scenarios. This is not verified subject consent or legal authorization. See [v0.21.0 release notes](RELEASE_NOTES_v0.21.0.md) and [the consent-assurance explainer](docs/agentic-ai/experimental-consent-assurance.md).


The [v0.20.0 experimental capability release](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/tag/v0.20.0) adds an experimental Delegated Creator profile, reproducible five-world cases, additional human/subject/vouching scenarios, Ed25519 statement-integrity tests, independent signer-binding evidence states, and an optional guarded C2PA validator interface. See the [detailed release notes](RELEASE_NOTES_v0.20.0.md).

**Assurance boundary:** These are feasibility and local conformance-evidence experiments, not CAWG-endorsed delegated-creator rules, legal authorization, verified enterprise identity, trusted signing time, or independently demonstrated C2PA/TRQP interoperability. The stable verifier APIs and operational profiles remain separate. [Issue #75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75) tracks remaining independent evidence.

**For reproducibility:** use the versioned release/tag rather than later changes on `main`.

## Experimental consent-evidence boundary (v0.21.0)

The repository also includes an independent, **non-authoritative** consent-evidence evaluator. It distinguishes claims about a represented person's consent from the actor's delegated authority and keeps historical use, withdrawal and current permissibility separate. All input evidence and times are caller-supplied; `assured_consent` remains indeterminate. The two synthetic integrated cases are reproducible with `python scripts/run_taskforce_consent_demo.py`. See the [experimental consent assurance documentation](docs/agentic-ai/experimental-consent-assurance.md). These additions do not change stable verifier APIs or close [#75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75).

## Start here

- [Guided learning paths](docs/guided-learning.md)
- [Non-technical overview](docs/NON_TECHNICAL_OVERVIEW.md)
- [Explainer presentation v4](docs/presentation-v4.md) (20 slides; pinned to v0.20.0)
- [Historical explainer v3](docs/presentation.md) (17 slides; v0.19.2)
- [Quickstart](QUICKSTART.md)
- [Operator decision and replay walkthrough](docs/operator-decision-replay-walkthrough.md)
- [HTTP to audit bundle adoption journey](docs/http-to-audit-bundle-adoption-journey.md)
- [Operational failure, correction, and redress](docs/operational-failure-correction-redress.md)
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

After the first verification, use the [operator walkthrough](docs/operator-decision-replay-walkthrough.md) to interpret the decision boundary, reason codes, evidence outputs, replay bundle, and correction lineage. For a production-style service integration, continue through the [HTTP-to-audit-bundle journey](docs/http-to-audit-bundle-adoption-journey.md) and then the [failure/correction/redress journey](docs/operational-failure-correction-redress.md).

## Validation and assurance evidence

Run the complete repository gate:

```bash
make validate
```

The gate validates repository governance and documentation integrity, the OpenAPI contract, JSON examples, walkthrough manifests, executable adoption journey contracts, the TRQP portfolio integration contract, and the Python test suite. Release-specific checks remain available independently:

```bash
python scripts/validate_portfolio_contract.py
python scripts/validate_adoption_journeys.py
python scripts/validate_feed_descriptors.py
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
python scripts/export_conformance_pack.py --check
# Checksums are generated for the checked-out source tree, not committed:
python scripts/generate_release_checksums.py
python scripts/generate_release_checksums.py --check
```

The checksum manifest validates selected release-evidence inputs for the
current checkout; it is not a checksum of the built wheel or source archive.
For immutable v0.21.0 publication evidence, use the
[checksum asset attached to the release](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/download/v0.21.0/checksums-v0.21.0.json)
and pin the matching source tag. The published manifest is deliberately not
stored as a generated file on `main`.

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
| `examples/` | canonical requests, receipts, audit bundles, walkthrough scenarios, and executable adoption journey contracts |
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
- **Enforcement:** CI, schema validation, conformance fixtures, revocation handling, portfolio-contract validation, adoption-journey validation, and release checks operationalize the stated controls.
- **Revocation and supersession:** corrected results and releases create new evidence; historical receipts are not rewritten.
- **Auditability:** receipts, bundles, manifests, integration contracts, journey contracts, and checksums provide machine-verifiable evidence.

See [`PROJECT-STATUS.yaml`](PROJECT-STATUS.yaml), [`SECURITY.md`](SECURITY.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and [`AI_USAGE.md`](AI_USAGE.md).

## Release

Latest release notes: [`RELEASE_NOTES_v0.21.0.md`](RELEASE_NOTES_v0.21.0.md)  
Changelog: [`CHANGELOG.md`](CHANGELOG.md)  
Roadmap: [`ROADMAP.md`](ROADMAP.md)

## License

MIT. See [`LICENSE`](LICENSE).

## Agentic AI assurance

The walkthrough portfolio includes a cross-cutting [Agentic AI Assurance](docs/agentic-ai/index.md) model that treats agents as delegated actors rather than trusted identities. It covers producer, submitter, verifier, orchestrator, proxy, and decision roles; binds actions to principals, mandates, scope, temporal validity, revocation, and replay evidence; and includes three executable archetypes under `examples/agent-*`.
