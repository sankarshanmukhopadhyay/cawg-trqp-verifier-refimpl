---
layout: default
title: "Cultural Heritage and Archive Ingest"
parent: "Walkthroughs"
nav_order: 23
description: "Authenticated digitization and delegated ingest for archives and cultural heritage collections."
---
# Cultural Heritage and Archive Ingest

## Purpose and decision boundary

This walkthrough shows how CAWG-derived content-authenticity signals can be combined with TRQP-resolved authority to make a narrow, replayable governance decision.

> **May this digitized asset be ingested as an authenticated contribution to the identified collection under the recorded custodial and digitization authority?**

The result does not adjudicate ownership, cultural authority, copyright, historical truth, or authenticity of the physical object; those remain governed by the institution and relevant communities.

## Plain-language summary

A museum, archive, digitization partner, researcher, or community contributor submits a digitized cultural-heritage asset for ingest. The archive needs to know whether the contributor is authorized for the identified collection or custodial context, whether the digitization/provenance evidence is adequate, and whether corrections can be made without erasing history.

A positive result means **the asset may be ingested as an authenticated contribution under the recorded custodial and digitization authority**. It does not settle ownership, cultural authority, intellectual-property rights, restitution claims, or the historical interpretation of the object. Those require separate governance and, often, consultation.

## At-a-glance governance flow

```mermaid
flowchart LR
    A[Capture or submit media with provenance] --> B[Validate and normalize authenticity signal]
    B --> C[Resolve authority, delegation, scope, and trust state]
    C --> D{Authorized for this action and context?}
    D -- Yes --> E[Allow governed workflow intake]
    D -- No --> F[Deny]
    D -- Stale or conflicting --> G[Indeterminate or review]
    E --> H[Issue receipt and preserve replay inputs]
    F --> H
    G --> H
    H --> I[Correction creates superseding receipt]
```

The key architectural separation is between **content provenance**, **authority to perform the action**, and the **downstream substantive decision**.


## Cross-functional interaction view

This swimlane-style interaction view shows how evidence moves between the submitting actor, the relying workflow, provenance validation, governed authority resolution, and the bounded operational decision.

```mermaid
sequenceDiagram
    participant S as Archive Submitter
    participant W as Archive Ingest Workflow
    participant C as CAWG/C2PA Validator
    participant V as TRQP Verifier
    participant A as Authority Sources

    S->>W: Submit asset/evidence + declared context
    W->>C: Validate provenance and normalize input
    C-->>W: Provenance findings
    W->>V: Verify requested action, scope, and policy
    V->>A: Resolve recognition, delegation, revocation, and freshness
    A-->>V: Current trust state
    V-->>W: allow / deny / review + evidence
    W-->>S: Receipt, correction route, or next-step request
```

## Governed decision state model

This state model keeps the governance lifecycle explicit so authorization, scope failure, revocation, stale trust state, conflict, and superseding correction are visible rather than collapsed into a single pass/fail result.

```mermaid
stateDiagram-v2
    [*] --> Pending

    Pending --> Authorized: provenance valid + authority current + scope satisfied
    Pending --> ScopeMismatch: actor recognized / requested action outside scope
    Pending --> Revoked: authority or delegation revoked
    Pending --> Stale: trust state unavailable or not fresh enough
    Pending --> Conflict: material authorities disagree

    Authorized --> Allowed: positive governed outcome
    ScopeMismatch --> Denied: deny or hold
    Revoked --> Denied: deny
    Stale --> Review: review / indeterminate
    Conflict --> Review: escalate

    Allowed --> Corrected: material evidence corrected
    Denied --> Corrected: material evidence corrected
    Review --> Corrected: authoritative correction supplied

    Corrected --> Pending: re-evaluate with updated inputs

    Allowed --> [*]
    Denied --> [*]
    Review --> [*]
```

## Why this workflow needs verifiable governance

Archive material is long-lived and may outlast the systems and institutions that first ingested it. That makes provenance, authority lineage, correction, and non-destructive history especially important. A digitization vendor may be authorized to capture but not to change descriptive metadata; a contributor may be recognized but outside the relevant collection mandate.

CAWG-TRQP can make those roles and boundaries explicit at ingest time. The resulting receipt and replay bundle preserve which authority and policy justified the original admission even if the catalog record is later corrected or the custodial context changes.

## Roles in the workflow

| Role | Responsibility | Evidence expected |
|---|---|---|
| Digitization operator | Captures or transforms the collection item | Provenance and transformation declaration |
| Custodial institution | Defines collection, operator, and use scope | Recognition/delegation and collection policy |
| Archive platform | Accepts or routes the asset | Decision receipt and reason codes |
| Rights or community stakeholder | May challenge metadata, authority, or permitted use | Correction/redress reference |
| Preservation auditor | Replays ingest and supersession history | Pinned evidence and lineage |



## System components mapped to workflow concepts

| Workflow concept | Verifier concept | Practical meaning |
|---|---|---|
| Collection/object identifier | Resource scope | Binds contribution authority to the intended heritage asset or collection |
| Custodian/digitization mandate | Recognition/delegation | Shows who may digitize, describe, or submit the material |
| Ingest/transformation policy | Action and process scope | Separates capture, metadata editing, and archival admission rights |
| Custodial authority change | Revocation/supersession | Prevents obsolete mandates governing new actions |
| Catalog correction | Superseding receipt | Preserves the historical ingest decision while recording updated evidence |

## Governance concerns

- **Collection-specific authority:** MUST be represented explicitly in policy, context, evidence, or review routing.
- **Declared restoration or transformation:** MUST be represented explicitly in policy, context, evidence, or review routing.
- **Rights and culturally sensitive access constraints:** MUST be represented explicitly in policy, context, evidence, or review routing.
- **Long-term correction and supersession lineage:** MUST be represented explicitly in policy, context, evidence, or review routing.

## End-to-end sequence

1. Validate the content-authenticity input and normalize only the fields needed by the relying workflow.
2. Bind the request to the specific resource, action, purpose, jurisdiction/location, and decision time.
3. Resolve recognition and every material delegation hop rather than treating identity or recognition as authorization.
4. Evaluate revocation and freshness according to the selected verifier profile.
5. Return `allow`, `deny`, `indeterminate`, or `review` with a stable reason code.
6. Issue a minimized decision receipt that pins policy, authority evidence, verifier version, and decision time.
7. Preserve replay inputs. Any material correction or supersession produces a new linked receipt.

## Decision and failure matrix

| Condition | Expected outcome | Governance meaning |
|---|---|---|
| Recognized, valid delegation, in scope | `allow` | Evidence may enter the governed downstream workflow |
| Recognized but wrong action/resource/context | `deny` | Recognition never substitutes for authorization |
| Authority/delegation revoked at decision time | `deny` | Revocation is enforceable |
| Required trust state stale/unavailable | `indeterminate` | Missing evidence is not silently trusted |
| Authoritative sources conflict | `review` | Conflict remains visible to a human/institutional control |
| Material metadata or authority evidence corrected | new decision | Historical evidence remains immutable |

## Runnable evidence package

The companion directory [`examples/cultural-heritage-archive-ingest/`](../../examples/cultural-heritage-archive-ingest/README.md) contains the machine-readable scenario contract and expected outcomes. Validate it with:

```bash
python scripts/validate_walkthrough_examples.py
```

## What evidence is produced

- scoped decision and stable reason code;
- authority, delegation, and revocation evidence references;
- policy/profile epoch and decision time;
- minimized decision receipt;
- replay inputs and correction lineage; and
- review/redress reference where the result is contested or non-deterministic.

## What can be tested

| Test question | Artifact or command |
|---|---|
| Do the walkthrough diagrams and required reader-facing sections pass quality validation? | `python scripts/validate_walkthrough_quality.py` |
| Do Mermaid flow, interaction, and state diagrams pass structural validation? | `python scripts/validate_walkthrough_diagrams.py` |
| Do machine-readable walkthrough manifests contain the common lifecycle cases? | `python scripts/validate_walkthrough_examples.py` |
| Do shipped example artefacts remain structurally valid? | `python scripts/validate_examples.py` |
| Does the complete repository validation surface pass? | `make validate` |

## Why this improves adoption

This walkthrough is easier to adopt when the governance value is expressed in familiar operational terms:

- archives can explain ingest decisions to curators, contributors, and auditors without exposing internal system details;
- digitization partners can receive narrowly scoped authority rather than broad repository access;
- corrections preserve historical evidence instead of rewriting the decision trail;
- future provenance or restitution research can distinguish technical ingest authority from broader ownership or cultural claims.

## Governance interpretation

Cultural-heritage governance cannot be reduced to technical authorization. The verifier can show why a digitized contribution was accepted under a custodial and process policy, but questions of title, cultural authority, ethics, restitution, and interpretation remain with the institutions and communities empowered to decide them.

The strength of the model is that it records one layer of authority without pretending that layer exhausts the governance of the object.

## Agentic AI Variant

Introducing an agent into **Cultural Heritage and Archive Ingest** changes the assurance problem from actor recognition alone to delegated-action assurance. Apply the common [Agentic AI Assurance model](../agentic-ai/index.md) and treat agent identity as necessary but insufficient evidence.

| Agentic control | Walkthrough requirement |
|---|---|
| Agent role | Model the agent explicitly as **digitization/producer agent, metadata submitter, verifier, or archive-ingest orchestrator**; authority in one role MUST NOT imply authority in another. |
| Principal | Bind the agent to **archive, museum, custodian, donor, rights holder, or cultural authority** and retain the principal reference in the decision evidence. |
| Delegated authority | Verify a mandate for the exact requested operation; authentication or recognition of the agent alone is not authorization. |
| Scope | Enforce **collection/item, digitization operation, restoration class, rights/access purpose, cultural restrictions, and retention/correction policy** as applicable to the transaction. |
| Tool/sub-agent chain | Where the agent invokes tools or downstream agents, retain evidence of material calls and reject unauthorized sub-delegation. |
| Revocation | Evaluate principal and delegation state at the decision time; revoked or expired authority cannot authorize a new action. |
| Failure | Preserve explicit `deny`, `review`, and `indeterminate` outcomes rather than coercing uncertainty into permission. |
| Audit and redress | Retain agent, principal, mandate, policy epoch, provenance/authority evidence, and a correction or challenge route sufficient for replay. |

Agent authority to digitize or restore an item does not imply authority to publish it, alter historically significant characteristics, change rights metadata, or override culturally sensitive access rules.

### Agentic conformance probes

In addition to the walkthrough's existing tests, exercise an authenticated agent with no mandate, a valid mandate with an out-of-scope action, revoked/expired delegation, prohibited sub-delegation or tool use, stale/conflicting authority state, and a corrected input that requires a superseding receipt.

## Operational assurance contract

An implementation claiming this walkthrough should demonstrate that:

1. scope is evaluated across action, resource, context, and decision time;
2. revocation is applied to the historical decision time being evaluated;
3. stale or conflicting state cannot yield an implicit positive decision;
4. replay over identical pinned inputs yields the same outcome and reason code; and
5. corrections are additive and linked rather than destructive.

## What this walkthrough does not prove

The result does not adjudicate ownership, cultural authority, copyright, historical truth, or authenticity of the physical object; those remain governed by the institution and relevant communities. The relying organization remains accountable for the downstream legal, professional, safety, editorial, or policy judgment.
