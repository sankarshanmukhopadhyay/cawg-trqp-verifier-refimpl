---
layout: default
title: "AI-Assisted Property Listing Images"
parent: "Walkthroughs"
nav_order: 4
---
# AI-Assisted Property Listing Image Verification

Property listings increasingly use generative staging, object removal, lighting correction, and synthetic views. These techniques can improve presentation, but they can also misrepresent room dimensions, structural condition, views, fixtures, damage, or amenities. The governance problem is therefore not merely whether AI was used. It is whether the actor was authorized, the transformation was declared, the policy was enforceable, and the resulting decision can be challenged and replayed.

CAWG/C2PA can provide provenance and transformation assertions. TRQP can determine whether the realtor, seller mandate, issuer, and marketplace authority are recognized and current. Together, they enable a marketplace to enforce a scoped policy rather than relying on an unverified badge or a free-text declaration.

## Decision boundary

This workflow does not treat content credentials as proof that a property matches the image. Physical accuracy still requires inspections, surveys, seller disclosures, and applicable legal remedies. CAWG-TRQP instead establishes a verifiable chain for who submitted the image, what was declared, which authority applied, and why the platform accepted, labelled, held, or rejected it.

## At-a-glance governance flow

```mermaid
flowchart LR
    A[Realtor submits listing image and mandate] --> B[Marketplace validates provenance and AI-edit declarations]
    B --> C[Verifier checks realtor status seller mandate and policy]
    C --> D{Publication conditions satisfied?}
    D -- Yes --> E[Publish with required disclosure]
    D -- No --> F[Reject the listing image]
    D -- Missing or conflicting --> G[Hold for review]
    E --> H[Issue receipt and correction route]
    F --> H
    G --> H
```

The flow governs authorization and disclosure while leaving physical property accuracy to inspections, surveys, and legal duties.


## Cross-functional interaction view

This swimlane-style interaction view shows how evidence moves between the submitting actor, the relying workflow, provenance validation, governed authority resolution, and the bounded operational decision.

```mermaid
sequenceDiagram
    participant S as Realtor / Brokerage
    participant W as Marketplace Listing Workflow
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

## Actors and authority

| Actor | Authority or responsibility |
|---|---|
| Seller | Grants and may revoke the listing mandate |
| Realtor or listing agent | Submits images within the mandate and applicable professional scope |
| Marketplace | Defines image policy and makes the publication decision |
| Realtor registry or licensing body | Supplies current recognition or disciplinary status where available |
| CAWG/C2PA validator | Validates manifest integrity and transformation assertions |
| TRQP verifier | Resolves recognition, mandate, policy, and revocation state |
| Buyer or affected party | Receives disclosure and can raise a challenge |
| Reviewer or regulator | Replays the decision from retained evidence |

## End-to-end flow

```mermaid
sequenceDiagram
    participant R as Realtor
    participant M as Marketplace
    participant C as CAWG/C2PA Validator
    participant V as TRQP Verifier
    participant A as Authority Sources
    participant B as Buyer or Reviewer

    R->>M: Submit listing image and seller mandate reference
    M->>C: Validate provenance and declared transformations
    C-->>M: Actor, asset, action, transformation and source bindings
    M->>V: Query recognition and scoped authorization
    V->>A: Check realtor status, mandate, policy and revocation
    A-->>V: Current authority state
    V-->>M: Decision inputs and evidence references
    M->>M: Apply marketplace image policy
    M-->>B: Publish with disclosure, hold, or reject
    M-->>B: Provide review and correction route
```

## Policy outcomes

| Condition | Outcome |
|---|---|
| Authorized realtor, active mandate, declared non-structural generative staging | Publish with prominent AI-edit disclosure |
| Missing provenance but no other adverse signal | Hold for manual review |
| Undeclared AI edit | Reject and preserve evidence |
| Fabricated view, amenity, room size, or structural condition | Reject and escalate under marketplace policy |
| Expired or revoked seller mandate | Reject |
| Conflicting actor or property binding | Quarantine and investigate |
| Stale registry or revocation data | Re-query or downgrade according to the declared failure policy |

## Controls that CAWG-TRQP adds

1. **Authority binding:** the image is connected to an actor who is recognized and authorized for the specific listing.
2. **Transformation accountability:** declared AI edits are bound to validated assertions rather than free-text claims.
3. **Scoped enforcement:** the policy distinguishes acceptable virtual staging from prohibited structural or factual fabrication.
4. **Revocation:** a withdrawn seller mandate or suspended actor can invalidate future publication decisions.
5. **Evidence and redress:** the marketplace produces a decision receipt that can be replayed during a buyer complaint, seller dispute, professional review, or regulatory inquiry.

## Runnable example

The machine-readable package is in [`examples/property-listing-ai-images`](../../examples/property-listing-ai-images/README.md). Its expected result is `conditionally_trusted`: the image may be published only with a prominent disclosure because generative staging was used.

## Assurance tests

A conforming implementation should test at least:

- authorized and unauthorized realtors;
- active, expired, and revoked seller mandates;
- declared and undeclared generative edits;
- allowed non-structural staging and prohibited structural alteration;
- mismatched listing and property identifiers;
- stale or unavailable authority sources;
- disclosure rendering and accessibility;
- evidence retention, correction, and appeal replay.

## Agentic AI Variant

Introducing an agent into **AI-Assisted Property Listing Image Verification** changes the assurance problem from actor recognition alone to delegated-action assurance. Apply the common [Agentic AI Assurance model](../agentic-ai/index.md) and treat agent identity as necessary but insufficient evidence.

| Agentic control | Walkthrough requirement |
|---|---|
| Agent role | Model the agent explicitly as **producer, submitter, verifier, or buyer-side orchestrator**; authority in one role MUST NOT imply authority in another. |
| Principal | Bind the agent to **seller, brokerage, marketplace, or buyer** and retain the principal reference in the decision evidence. |
| Delegated authority | Verify a mandate for the exact requested operation; authentication or recognition of the agent alone is not authorization. |
| Scope | Enforce **listing/property identifier, permitted transformation class, publication channel, purpose, and mandate validity** as applicable to the transaction. |
| Tool/sub-agent chain | Where the agent invokes tools or downstream agents, retain evidence of material calls and reject unauthorized sub-delegation. |
| Revocation | Evaluate principal and delegation state at the decision time; revoked or expired authority cannot authorize a new action. |
| Failure | Preserve explicit `deny`, `review`, and `indeterminate` outcomes rather than coercing uncertainty into permission. |
| Audit and redress | Retain agent, principal, mandate, policy epoch, provenance/authority evidence, and a correction or challenge route sufficient for replay. |

An AI agent may stage or enhance an image only within the seller/brokerage mandate; a buyer-side verifier agent may authenticate provenance and mandate state but cannot infer that the physical property matches the image or autonomously waive inspection/legal duties.

### Agentic conformance probes

In addition to the walkthrough's existing tests, exercise an authenticated agent with no mandate, a valid mandate with an out-of-scope action, revoked/expired delegation, prohibited sub-delegation or tool use, stale/conflicting authority state, and a corrected input that requires a superseding receipt.

## Operational assurance contract

This walkthrough is testable as a bounded governance decision rather than as a claim that the underlying content is true.

| Control point | Required behavior | Evidence |
|---|---|---|
| Decision | Evaluate **Listing-image acceptance** only | Stable outcome and reason code |
| Authority | Resolve brokerage or delegated agent authority, delegation, scope, and current status | Authority and delegation references |
| Freshness | Apply the required revocation and trust-state freshness rules | Timestamped trust-state evidence |
| Policy | Pin the listing disclosure policy epoch used for evaluation | Policy identifier/version or digest |
| Failure | Fail visibly on stale, unavailable, ambiguous, or conflicting authority state | `indeterminate`/`review` receipt rather than implicit trust |
| Correction | Preserve the original decision and issue a superseding receipt when material inputs change | Immutable receipt lineage |
| Handoff | Pass the result into **property listing workflow** without transferring accountability to the verifier | Relying-party disposition/audit reference |

### Conformance assertions

An implementation claiming this walkthrough should be able to demonstrate that:

1. recognition alone never grants the requested action when scope or delegation is absent;
2. a revoked authority or delegation cannot produce a positive decision for the affected decision time;
3. stale or conflicting trust state is surfaced explicitly and never silently coerced to `allow`;
4. identical pinned inputs replay to the same governed outcome and reason code; and
5. a correction produces a new decision linked to, rather than overwriting, the historical receipt.

