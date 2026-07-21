---
layout: default
title: "Industry Body Decision Brief"
parent: "Industry Adoption"
nav_order: 1
---
# Industry Body Decision Brief

## The decision in one sentence

Approve a bounded interoperability pilot that tests whether a platform can verify, through CAWG-derived evidence and TRQP, that a recognized distributor is authorized by a recognized label to deliver a specified recording within a defined territory, platform, and time period.

## The institutional problem

Industry bodies already coordinate membership, recognition, codes of practice, accreditation, rights-management conventions, technical policy, and enforcement expectations. These forms of authority are usually communicated through documents, databases, contracts, and bilateral integrations. They are rarely available as interoperable, machine-verifiable decisions at the moment a platform must act.

Content provenance addresses a different problem. CAWG/C2PA evidence can establish that assertions are cryptographically bound to an asset and can record who declared what. It does not, by itself, answer whether the declaring or submitting actor was authorized to distribute, classify, license, transform, or enforce against that asset.

The CAWG-TRQP reference implementation demonstrates how those two layers can be connected without requiring the industry body to own every underlying record.

## What becomes possible

A relying party can ask bounded questions such as:

- Is this issuer recognized by an accepted music-industry authority?
- Is this distributor authorized by that issuer to deliver this recording?
- Does the authority apply to this platform, territory, purpose, and time period?
- Has the authority expired, been revoked, or become disputed?
- Can the decision be explained and independently replayed?

The outcome is not a universal declaration of ownership. It is a scoped trust decision supported by versioned policy and evidence.

## Potential roles for an industry body

| Role | Responsibility | Evidence produced |
|---|---|---|
| Governance authority | Define participation, authority, revocation, and appeal rules | Governance charter and decision-rights matrix |
| Recognition authority | Determine which registries and sector authorities are accepted | Recognition policy and signed recognition data |
| Profile custodian | Maintain sector actions, resources, context keys, and reason codes | Versioned application profile and compatibility statement |
| Trust-gateway operator | Route queries to recognized registries while preserving federation | Mediation traces and gateway-route evidence |
| Assurance coordinator | Define conformance levels and independent assessment requirements | Test vectors, conformance reports, assurance manifests |
| Appeal authority | Establish correction, review, and restoration processes | Appeal records and replayable decision evidence |
| Pilot convenor | Coordinate members, platforms, technical operators, and assessors | Pilot charter, risk register, and final assessment |

The recommended institutional posture is **federated governance**, not a single centralized registry containing all music-sector facts.

## What this architecture does not do

It does not:

- determine copyright ownership conclusively;
- replace contracts, statutory processes, courts, or collective-bargaining arrangements;
- prove that every factual claim about a recording is true;
- make an unknown result equivalent to infringement or fraud;
- require confidential contracts or complete manifests to be disclosed;
- remove final responsibility from the platform or other relying party;
- authorize a named industry body to act outside its agreed scope.

## Why start with authorized distribution

Distribution authority is a good first pilot because it has a bounded actor, action, resource, issuer, relying party, time period, and revocation path. It can create measurable operational value without attempting to resolve the entire rights landscape.

The first pilot should test:

1. recognized label identity;
2. recognized distributor identity;
3. scoped distribution authorization;
4. territory, platform, and time limits;
5. expiry and revocation;
6. reasoned hold and rejection states;
7. decision receipts and replay;
8. appeal and correction.

## Decisions required from the industry body

| Decision | Why it matters |
|---|---|
| Pilot authority and scope | Prevents the pilot from becoming an implied industry-wide mandate |
| Registry and gateway operators | Establishes operational responsibility and separation of duties |
| Accepted identifier types | Ensures actors and issuers can be resolved consistently |
| Recognition policy | Defines whose assertions and registries are accepted |
| Distribution action and resource semantics | Prevents inconsistent interpretations across participants |
| Freshness and revocation policy | Sets the trade-off between current lookup, cache, resilience, and risk |
| Evidence retention | Determines what can be audited without exposing unnecessary commercial data |
| Appeal and correction process | Prevents automated decisions from becoming unreviewable exclusion mechanisms |
| Independent assessment | Produces credible evidence for adoption, revision, or termination |

## Requested executive action

Approve a limited pilot charter with named participants, a fixed duration, explicit success and stop criteria, a non-normative technical profile, and independent assessment. Do not approve production claims or sector-wide authority until the pilot produces conformance, operational, governance, and redress evidence.
