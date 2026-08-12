---
layout: default
title: "Legal and Administrative Evidence Submission"
parent: "Walkthroughs"
nav_order: 21
description: "Governed intake of authenticated media into legal or administrative proceedings."
---
# Legal and Administrative Evidence Submission

## Purpose and decision boundary

This walkthrough shows how CAWG-derived content-authenticity signals can be combined with TRQP-resolved authority to make a narrow, replayable governance decision.

> **May this media asset be accepted into the identified proceeding as an authenticated submission from an authorized actor under the recorded rules?**

Acceptance into an evidence workflow is not a ruling on admissibility, authenticity in the legal sense, probative value, ownership, or the merits of a proceeding.

## Plain-language summary

A lawyer, agency officer, party, or authorized representative submits media into a legal or administrative proceeding. The intake service needs to know whether the submitter may act for the identified matter, whether the evidence is bound to the correct case and filing action, and whether that authority was current when submitted.

A positive result means **the media may be accepted into the identified intake process as an authenticated submission from an authorized actor**. It does not decide admissibility, evidentiary weight, authenticity in the legal sense, privilege, relevance, or the merits of the proceeding. Those remain with the competent tribunal or administrative authority.

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
    participant S as Filer or Authorized Representative
    participant W as Court / Agency Intake
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

Legal systems already distinguish filing authority from the substantive consequence of a filing. Digital evidence should preserve the same separation. A file can have intact provenance but arrive from an unauthorized representative, be submitted to the wrong case, or rely on a mandate that was revoked before the filing time.

CAWG-TRQP makes the filing authority check machine-verifiable while preserving the tribunal’s independence. It also creates a precise audit trail for disputes about who filed what, under which authority, and which policy version governed the intake decision.

## Roles in the workflow

| Role | Responsibility | Evidence expected |
|---|---|---|
| Submitting party | Provides media and declared context | Provenance plus case/submission reference |
| Court or tribunal authority | Defines authorized submission channels and roles | Recognition, delegation, and procedural policy |
| Evidence intake service | Performs the bounded acceptance decision | Decision receipt and reason codes |
| Opposing/affected party | May challenge provenance, authority, or handling | Challenge and correction reference |
| Auditor | Replays intake state without rewriting history | Pinned inputs and receipt lineage |



## System components mapped to workflow concepts

| Workflow concept | Verifier concept | Practical meaning |
|---|---|---|
| Case/proceeding identifier | Resource scope | Binds the submission to the correct matter |
| Counsel/representative authority | Recognition/delegation | Shows who may file for the party or agency |
| Filing/evidence action | Action scope | Separates permission to submit from admissibility or merits |
| Withdrawal/substitution of authority | Revocation state | Prevents former representatives making new authorized filings |
| Clerk/tribunal review | Review disposition | Routes uncertain authority without pre-judging the evidence |

## Governance concerns

- **Case-specific scope:** MUST be represented explicitly in policy, context, evidence, or review routing.
- **Chain-of-custody continuity:** MUST be represented explicitly in policy, context, evidence, or review routing.
- **Role or counsel substitution:** MUST be represented explicitly in policy, context, evidence, or review routing.
- **Post-submission corrections without evidence erasure:** MUST be represented explicitly in policy, context, evidence, or review routing.

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

The companion directory [`examples/legal-evidence-submission/`](../../examples/legal-evidence-submission/README.md) contains the machine-readable scenario contract and expected outcomes. Validate it with:

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

- filers receive explainable intake failures tied to scope or authority;
- courts/agencies can automate routine filing checks without delegating adjudication to the verifier;
- representation changes can be enforced at the authorization layer;
- later procedural review can replay the trust and policy state used when the filing entered the system.

## Governance interpretation

The verifier is an intake assurance component, not a judicial decision-maker. It can answer whether the configured submission conditions were met; only the competent legal or administrative authority determines admissibility, weight, entitlement, liability, or remedy.

This is a useful example of executable governance because it preserves familiar institutional separation while giving the authority check a reproducible technical form.

## Agentic AI Variant

Introducing an agent into **Legal and Administrative Evidence Submission** changes the assurance problem from actor recognition alone to delegated-action assurance. Apply the common [Agentic AI Assurance model](../agentic-ai/index.md) and treat agent identity as necessary but insufficient evidence.

| Agentic control | Walkthrough requirement |
|---|---|
| Agent role | Model the agent explicitly as **submitter, evidence-packaging agent, verifier, or case-workflow orchestrator**; authority in one role MUST NOT imply authority in another. |
| Principal | Bind the agent to **party, counsel, agency, tribunal, or other competent authority** and retain the principal reference in the decision evidence. |
| Delegated authority | Verify a mandate for the exact requested operation; authentication or recognition of the agent alone is not authorization. |
| Scope | Enforce **case/proceeding, recipient, evidence class, filing operation, purpose, deadline, and correction rights** as applicable to the transaction. |
| Tool/sub-agent chain | Where the agent invokes tools or downstream agents, retain evidence of material calls and reject unauthorized sub-delegation. |
| Revocation | Evaluate principal and delegation state at the decision time; revoked or expired authority cannot authorize a new action. |
| Failure | Preserve explicit `deny`, `review`, and `indeterminate` outcomes rather than coercing uncertainty into permission. |
| Audit and redress | Retain agent, principal, mandate, policy epoch, provenance/authority evidence, and a correction or challenge route sufficient for replay. |

A valid document submitted by an authenticated agent is not an authorized filing unless the principal-agent mandate covers the specific proceeding and submission operation; verification does not decide admissibility or probative value.

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

Acceptance into an evidence workflow is not a ruling on admissibility, authenticity in the legal sense, probative value, ownership, or the merits of a proceeding. The relying organization remains accountable for the downstream legal, professional, safety, editorial, or policy judgment.
