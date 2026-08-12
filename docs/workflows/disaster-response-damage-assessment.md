---
layout: default
title: "Disaster Response Damage Assessment"
parent: "Walkthroughs"
nav_order: 20
description: "Authenticity and scoped authority for time-sensitive disaster damage imagery."
---
# Disaster Response Damage Assessment

## Purpose and decision boundary

This walkthrough shows how CAWG-derived content-authenticity signals can be combined with TRQP-resolved authority to make a narrow, replayable governance decision.

> **May this image or video be accepted as authenticated field evidence for the identified incident, location, response programme, and decision time?**

The result can authenticate provenance and scoped collection authority; it does not establish the severity of damage, entitlement to aid, causation, or the truth of every contextual claim.

## Plain-language summary

A field assessor submits images or video during a disaster response. Emergency coordinators need to know whether the assessor was authorized for the incident and location, whether the evidence is tied to the correct response program, and whether authority state is current enough for operational use.

A positive result means **the material may be accepted as authenticated field evidence for the identified incident and workflow**. It does not prove the final damage estimate, funding eligibility, safety of a structure, or entitlement to relief. The verifier makes the field-evidence admission decision explicit so urgent operations do not have to rely only on informal rosters or unverifiable media channels.

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
    participant S as Field Assessor
    participant W as Emergency Coordination Workflow
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

Disaster response combines urgency, rapidly changing assignments, intermittent connectivity, multiple agencies, and high volumes of citizen and professional media. A recognized assessor may be assigned to a different zone, an agency mandate may change during the response, and stale trust data may be operationally significant.

The walkthrough shows how the verifier can encode incident, location, program, time, and delegation scope while preserving `review` or `indeterminate` when the necessary trust state is unavailable. This supports rapid action without hiding the uncertainty created by the environment.

## Roles in the workflow
| Role | Responsibility | Evidence expected |
|---|---|---|
| Field collector | Captures and submits incident imagery | CAWG/C2PA-derived provenance and assignment context |
| Response authority | Defines authorized collectors, geographic/incident scope, and permitted use | Signed recognition, delegation, and policy state |
| Operations centre | Uses the result for triage or case routing | Decision receipt and reason codes |
| Affected community member | May contest attribution, location, or use | Correction/redress reference |
| Assurance reviewer | Replays the historical decision | Pinned trust state and audit evidence |



## System components mapped to workflow concepts

| Workflow concept | Verifier concept | Practical meaning |
|---|---|---|
| Incident/response program | Resource and purpose scope | Binds evidence to the declared emergency context |
| Assessor/team assignment | Recognition/delegation | Shows who may collect or submit evidence |
| Zone/location | Jurisdiction scope | Prevents an assignment being reused outside its operational area |
| Assignment withdrawal | Revocation state | Stops a superseded team mandate from authorizing new evidence |
| Emergency operations review | Review disposition | Allows urgent escalation without silently treating uncertainty as trust |
## Governance concerns

- **Incident and geographic scope:** MUST be represented explicitly in policy, context, evidence, or review routing.
- **Offline capture followed by delayed synchronization:** MUST be represented explicitly in policy, context, evidence, or review routing.
- **Rapid revocation after device or credential compromise:** MUST be represented explicitly in policy, context, evidence, or review routing.
- **Privacy minimization for affected persons:** MUST be represented explicitly in policy, context, evidence, or review routing.

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

The companion directory [`examples/disaster-response-damage-assessment/`](../../examples/disaster-response-damage-assessment/README.md) contains the machine-readable scenario contract and expected outcomes. Validate it with:

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

- operations centers can triage evidence from multiple teams using a consistent trust boundary;
- field personnel receive scope-specific outcomes rather than broad identity checks;
- inter-agency authority changes can be reflected in future decisions;
- after-action reviews can replay what authority and policy state was available during the response.

## Governance interpretation

Emergency conditions do not remove the need for governance; they make explicit delegation and failure policy more important. The verifier supports one bounded decision about field-evidence admission while emergency managers, engineers, relief authorities, and funders retain their own operational and substantive authorities.

The evidence record also helps distinguish what was knowable at decision time from information learned later, which is essential for fair after-action review.

## Agentic AI Variant

Introducing an agent into **Disaster Response Damage Assessment** changes the assurance problem from actor recognition alone to delegated-action assurance. Apply the common [Agentic AI Assurance model](../agentic-ai/index.md) and treat agent identity as necessary but insufficient evidence.

| Agentic control | Walkthrough requirement |
|---|---|
| Agent role | Model the agent explicitly as **producer/capture agent, submitter, verifier, assessor, or dispatch orchestrator**; authority in one role MUST NOT imply authority in another. |
| Principal | Bind the agent to **emergency authority, field organization, property holder, or response programme** and retain the principal reference in the decision evidence. |
| Delegated authority | Verify a mandate for the exact requested operation; authentication or recognition of the agent alone is not authorization. |
| Scope | Enforce **incident, location, collection task, aid programme, assessment class, geography, time window, and decision threshold** as applicable to the transaction. |
| Tool/sub-agent chain | Where the agent invokes tools or downstream agents, retain evidence of material calls and reject unauthorized sub-delegation. |
| Revocation | Evaluate principal and delegation state at the decision time; revoked or expired authority cannot authorize a new action. |
| Failure | Preserve explicit `deny`, `review`, and `indeterminate` outcomes rather than coercing uncertainty into permission. |
| Audit and redress | Retain agent, principal, mandate, policy epoch, provenance/authority evidence, and a correction or challenge route sufficient for replay. |

Evidence-generation authority, damage-assessment authority, and benefit/dispatch authority must remain independently expressible; one agent must not acquire all three simply by participating in the workflow.

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

The result can authenticate provenance and scoped collection authority; it does not establish the severity of damage, entitlement to aid, causation, or the truth of every contextual claim. The relying organization remains accountable for the downstream legal, professional, safety, editorial, or policy judgment.
