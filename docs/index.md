---
layout: default
title: "Home"
description: "Executable reference verifier for TRQP-integrated CAWG/C2PA content authenticity decisions."
nav_order: 1
permalink: /
---
# CAWG-TRQP Reference Implementation
{: .fs-9 }

An executable reference verifier that connects TRQP authority queries to
content-authenticity decisions, structured decision receipts, and
replayable audit evidence.
{: .fs-6 .fw-300 }

[Quickstart](../QUICKSTART.md){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[Non-Technical Overview](NON_TECHNICAL_OVERVIEW.md){: .btn .fs-5 .mb-4 .mb-md-0 .mr-2 }
[Presentation](presentation.md){: .btn .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## What this is

Content published under CAWG/C2PA carries assertions about who made it,
what process produced it, and what authority stands behind it. Those
assertions are only useful if something can turn them into a decision:
*should this asset be trusted, and why?*

This repository is a working implementation of that decision layer. It queries trust registries the way the [Trust Registry Query Protocol (TRQP)](trqp-alignment.md) describes, applies a declared verification profile, and produces a **decision receipt** — a structured, replayable record of what was checked, what was trusted, and why. Every decision can be exported as an **audit bundle** and independently replayed by a third party from pinned inputs, without needing to trust the verifier's live output.

It is not a demo that returns `true`/`false`. It is a reference for what an
accountable, testable, and interoperable verifier looks like.

## Who this is for

| If you are&hellip; | Start with |
|---|---|
| New to this space, or reviewing it for context (governance, editorial, program management) | [Presentation](presentation.md), [Non-Technical Overview](NON_TECHNICAL_OVERVIEW.md), then the [Photography Contest Walkthrough](workflows/photography-contest-verification.md) |
| A CAWG or C2PA participant deciding what must change for TRQP integration | [CAWG-to-TRQP Integration Enablement](cawg-trqp-integration-enablement.md), then [CAWG Implementation Playbook](industry-adoption/cawg-implementation-playbook.md), [CAWG Input Contract](cawg-input-contract.md), and [API Call Catalogue](api-call-catalogue.md) |
| An industry body or sector programme sponsor | [Industry Body Decision Brief](industry-adoption/industry-body-decision-brief.md), then the [Music-Industry Pilot Blueprint](industry-adoption/music-industry-pilot-blueprint.md) |
| A developer integrating a verifier into your own system | [Quickstart](../QUICKSTART.md), then [CAWG Input Contract](cawg-input-contract.md), [API Call Catalogue](api-call-catalogue.md), and [Integration Guide](INTEGRATION_GUIDE.md) |
| Standing up or operating a deployment | [Architecture](architecture.md), then [Deployment Guide](deployment-guide.md) |
| Reviewing assurance, evidence, or audit posture | [How TRQP Enables Assurance](how-trqp-enables-assurance.md), then [Decision Receipt Specification](decision-receipt-specification.md) and [Audit Bundle Profile](audit-bundle-profile.md) |
| Building or running a conformance/interoperability program | [Assurance Suite Ingestion](assurance-suite-ingestion.md), [Interoperability Vectors](interoperability-vectors.md), [Compatibility Matrix](compatibility-matrix.md) |
| Deciding whether to contribute, or reporting a security issue | [Governance](../GOVERNANCE.md), [Contributing](../CONTRIBUTING.md), [Security Policy](../SECURITY.md) |

## Industry adoption

For decision-makers and implementers exploring sector deployment, the [Industry Adoption](industry-adoption/index.md) package provides a decision brief, recorded-music application profile, CAWG implementation playbook, bounded pilot blueprint, executable walkthrough, canonical payloads, and machine-readable readiness gates.

## What it enables today

- **Profile-driven policy enforcement** — three schema-backed profiles (`standard`, `high_assurance`, `edge`) cover online, fail-closed, and offline-snapshot verification postures. See [Verifier Profiles](verifier-profiles.md).
- **Signed, attestable feed inputs** — policy, revocation, snapshot, and gateway-route feeds can be independently signed and validated before the verifier relies on them. See [Feed Descriptor Profile](feed-descriptor-profile.md) and [Descriptor Policy](descriptor-policy.md).
- **Replayable decisions** — every decision can be re-derived from pinned inputs by an independent party, producing a `matches: true/false` result rather than requiring blind trust in the original run. See [Reproducibility Guide](reproducibility-guide.md).
- **Structured, queryable evidence** — decision receipts and audit bundles are JSON Schema-backed artifacts, not free-text logs. See [Decision Receipt Specification](decision-receipt-specification.md) and [Audit Bundle Profile](audit-bundle-profile.md).
- **A deployable HTTP service** — a hardened Flask service exposes authorization, recognition, verification, and audit-bundle export over HTTP, with Docker packaging. See [HTTP Transport Patterns](http-transport-patterns.md) and [Deployment Guide](deployment-guide.md).
- **External conformance ingestion** — a machine-readable manifest lets other TRQP/CAWG verifier implementations and conformance suites consume this repository's fixtures directly. See [Assurance Suite Ingestion](assurance-suite-ingestion.md).

## What it holds the potential for

The [Roadmap](../ROADMAP.md) tracks this in detail, but the direction is: a redistribution-safe binary CAWG/C2PA parser behind the existing adapter boundary, a wider adversarial (negative) fixture library, production service packaging, and formal cross-repository alignment with the TRQP conformance suite and assurance hub — turning this reference implementation into one verified stage of a portfolio-wide, machine-verifiable trust pipeline. See [TRQP Adoption Path](trqp-adoption-path.md) for how this repository is meant
to sit alongside the protocol specification, the security/profile layer,
the conformance suite, and the assurance hub.

## Governance model, in one paragraph

The repository treats trust as **executable governance**: profile and
policy feeds determine *authority*; gateway-mediated flows preserve
*delegation* scope; revocation, descriptor policy, and transport
constraints provide *enforcement*; and decision receipts, audit bundles,
and replay bundles provide *evidence*. See [Governance](../GOVERNANCE.md)
for the full authority and decision-rights model.

## Current status

| Attribute | Value |
|---|---|
| Current release | v0.17.0 |
| Test suite | 79/79 passing |
| Validation gate | `make validate` — see [Contributing](../CONTRIBUTING.md) |
| Documentation | This site — see the section navigation on the left |
{: .note }


- [Scalability and performance](scalability-and-performance.md)
- [Cache, freshness, and revocation](cache-freshness-and-revocation.md)
- [High-volume deployment profile](high-volume-deployment-profile.md)

## Privacy and personal information

Deployers, privacy teams, and assurance reviewers should begin with the [Privacy and Personal Information](privacy/index.md) section. It covers data flow, role allocation, context minimization, evidence profiles, retention, correction, cross-border federation, and privacy threats.


## Threats and adversarial assurance

Security reviewers, operators, and governance authorities should use the [Threats and Risks](threats-and-risks/index.md) section for the system threat model, trust boundaries, attack scenarios, abuse cases, recovery procedures, and machine-readable residual-risk decisions.
