---
layout: default
title: "Insurance Claim Evidence"
parent: "Walkthroughs"
nav_order: 11
description: "Real-world CAWG-TRQP governance walkthrough."
---
# Insurance Claim Evidence

## Purpose and decision boundary

A policyholder or delegated representative submits property or vehicle damage imagery after a disaster. The insurer decides whether the material is sufficient for triage, inspection routing, or escalation, not whether the claim must be paid.

The decision is deliberately narrow:

> **May this asset be used for claim triage under the authority, scope, policy, and trust state recorded at decision time?**

A successful result does not establish factual truth, legal liability, professional judgment, product authenticity, clinical validity, or entitlement beyond that scoped action.

## Plain-language summary

A policyholder, repairer, or delegated representative submits damage images for an insurance claim. The insurer needs to know whether the evidence is bound to the correct claim and incident, whether the submitter is authorized for this stage of the process, and whether the authority and evidence are current enough to use for triage.

A positive result means **the material may be used for the defined claim-processing step**. It does not establish coverage, causation, fraud, liability, repair cost, or entitlement to payment. Those remain separate claims decisions. The verifier makes the intake authorization and evidence lineage reproducible so that a later adjuster, reviewer, or claimant can understand why the material entered the workflow.

## At-a-glance governance flow

```mermaid
flowchart LR
    A[Policyholder or delegate submits damage media] --> B[Insurer validates provenance and claim binding]
    B --> C[Verifier checks submitter authority and incident scope]
    C --> D{Evidence usable for this claim stage?}
    D -- Yes --> E[Allow triage or inspection routing]
    D -- No --> F[Deny or request corrected evidence]
    D -- Stale or conflicting --> G[Escalate to adjuster review]
    E --> H[Issue receipt and retain appeal evidence]
    F --> H
    G --> H
```

The decision authorizes use at a defined claim stage; it does not determine liability or require payment.


## Cross-functional interaction view

This swimlane-style interaction view shows how evidence moves between the submitting actor, the relying workflow, provenance validation, governed authority resolution, and the bounded operational decision.

```mermaid
sequenceDiagram
    participant S as Policyholder or Delegate
    participant W as Claims Intake Workflow
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

Claims workflows often mix self-submitted media, repair-shop evidence, adjuster inspections, and automated triage. The same image can be authentic but attached to the wrong claim, submitted by someone without authority, reused across incidents, or evaluated after a delegation has been revoked. When those checks are handled only through application permissions or manual review, the evidence supporting the decision is difficult to reconstruct.

CAWG-TRQP provides a bounded trust decision before substantive claims assessment. It can enforce claim binding, delegated submission authority, revocation, and freshness while keeping uncertainty visible. This helps the insurer move quickly without pretending that provenance or submitter authority resolves the claim itself.

## Roles in the workflow
| Role | Responsibility | Evidence expected |
|---|---|---|
| Submitter | Supplies the asset and declared context | CAWG/C2PA-derived integration signal |
| Governing authority | Defines who may perform `triage_claim` | Signed policy and recognition information |
| Relying service | Applies the decision to its own workflow | Decision receipt and reason codes |
| Affected party | May challenge metadata, authority, or use | Correction, appeal, or redress reference |
| Assurance reviewer | Replays and audits the decision | Pinned inputs and audit bundle |



## System components mapped to workflow concepts

| Workflow concept | Verifier concept | Practical meaning |
|---|---|---|
| Claim or policy number | Resource scope | Binds the evidence to the intended claim or insured asset |
| Policyholder/repairer authority | Recognition and delegation | Shows who may submit evidence and for which step |
| Incident/date window | Time and purpose scope | Prevents otherwise valid evidence being reused outside the authorized event |
| Withdrawn representation | Revocation state | Stops a former representative authorizing a new submission |
| Adjuster escalation | `review` / `indeterminate` outcome | Routes uncertain evidence without silently accepting it |
## Governance concerns

- **Delegated Submission:** represented as explicit policy, context, evidence, or review requirements.
- **Incident And Policy Binding:** represented as explicit policy, context, evidence, or review requirements.
- **Duplicate Image Detection:** represented as explicit policy, context, evidence, or review requirements.
- **Appeal And Correction:** represented as explicit policy, context, evidence, or review requirements.

## End-to-end sequence

1. Validate the content-authenticity input and normalize it into the CAWG-TRQP integration signal.
2. Resolve the actor, `insurer` authority source, and relevant delegation chain.
3. Evaluate `triage_claim` against asset, resource, jurisdiction, purpose, and time scope.
4. Check revocation, freshness, descriptor integrity, and any profile-specific fail-closed requirements.
5. Return `allow`, `deny`, `indeterminate`, or `review` with stable reason codes.
6. Issue a decision receipt that identifies the policy epoch, authority evidence, verifier version, and evidence minimization profile.
7. Preserve replay inputs. A corrected or superseding decision creates a new receipt rather than mutating the historical record.

## Required cases

| Case | Expected outcome | Assurance point |
|---|---|---|
| Authorized and in scope | `allow` | Positive path is reproducible |
| Recognized but scope mismatch | `deny` | Recognition is not authorization |
| Revoked authority | `deny` | Revocation is enforced |
| Stale or unavailable authority state | `indeterminate` or `review` | Missing evidence never silently becomes trusted |
| Conflicting authorities | `review` | Conflict is visible and routed |
| Corrected metadata | new decision | History remains immutable and auditable |

## Runnable evidence package

The companion directory [`examples/insurance-claim-evidence/`](../../examples/insurance-claim-evidence/README.md) contains a machine-readable scenario manifest and expected outcomes. Run:

```bash
python scripts/validate_walkthrough_examples.py
```

## What evidence is produced

- scoped decision and stable reason codes;
- authority, delegation, and revocation evidence references;
- policy and context-profile versions;
- minimized decision receipt;
- replay inputs and correction lineage; and
- an explicit review or redress route for contested decisions.

## What this walkthrough does not prove

This walkthrough does not convert provenance into truth and does not transfer institutional accountability to the verifier. The relying organization remains responsible for the lawful, proportionate, and procedurally fair use of the result.

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

- claimants get clearer reasons when evidence cannot be used;
- claims teams can separate evidence intake from coverage and payment adjudication;
- delegated repairers and representatives can be authorized narrowly instead of receiving broad account access;
- appeals and fraud reviews can replay the exact trust-state inputs used at triage.

## Governance interpretation

The verifier governs admission of evidence to a defined claims step; it does not decide the economic or legal consequence of the claim. The insurer remains accountable for coverage interpretation, fraud controls, valuation, fairness, and redress.

This division keeps authority proportional. A machine-verifiable authorization decision can accelerate intake while the higher-stakes adjudication remains subject to the insurer’s separately governed processes.

## Agentic AI Variant

Introducing an agent into **Insurance Claim Evidence** changes the assurance problem from actor recognition alone to delegated-action assurance. Apply the common [Agentic AI Assurance model](../agentic-ai/index.md) and treat agent identity as necessary but insufficient evidence.

| Agentic control | Walkthrough requirement |
|---|---|
| Agent role | Model the agent explicitly as **capture agent, claimant proxy, submitter, verifier, or claims-workflow orchestrator**; authority in one role MUST NOT imply authority in another. |
| Principal | Bind the agent to **claimant, insurer, adjuster, repairer, or authorized representative** and retain the principal reference in the decision evidence. |
| Delegated authority | Verify a mandate for the exact requested operation; authentication or recognition of the agent alone is not authorization. |
| Scope | Enforce **claim, insured asset/event, evidence class, submission operation, purpose, and validity window** as applicable to the transaction. |
| Tool/sub-agent chain | Where the agent invokes tools or downstream agents, retain evidence of material calls and reject unauthorized sub-delegation. |
| Revocation | Evaluate principal and delegation state at the decision time; revoked or expired authority cannot authorize a new action. |
| Failure | Preserve explicit `deny`, `review`, and `indeterminate` outcomes rather than coercing uncertainty into permission. |
| Audit and redress | Retain agent, principal, mandate, policy epoch, provenance/authority evidence, and a correction or challenge route sufficient for replay. |

Authenticated provenance and submission authority do not establish coverage, causation, damage quantum, fraud, or entitlement; claims adjudication requires separately governed authority.

### Agentic conformance probes

In addition to the walkthrough's existing tests, exercise an authenticated agent with no mandate, a valid mandate with an out-of-scope action, revoked/expired delegation, prohibited sub-delegation or tool use, stale/conflicting authority state, and a corrected input that requires a superseding receipt.

## Operational assurance contract

This walkthrough is testable as a bounded governance decision rather than as a claim that the underlying content is true.

| Control point | Required behavior | Evidence |
|---|---|---|
| Decision | Evaluate **Claim-evidence acceptance** only | Stable outcome and reason code |
| Authority | Resolve insurer or delegated adjuster authority, delegation, scope, and current status | Authority and delegation references |
| Freshness | Apply the required revocation and trust-state freshness rules | Timestamped trust-state evidence |
| Policy | Pin the claim-handling policy epoch used for evaluation | Policy identifier/version or digest |
| Failure | Fail visibly on stale, unavailable, ambiguous, or conflicting authority state | `indeterminate`/`review` receipt rather than implicit trust |
| Correction | Preserve the original decision and issue a superseding receipt when material inputs change | Immutable receipt lineage |
| Handoff | Pass the result into **claims assessment** without transferring accountability to the verifier | Relying-party disposition/audit reference |

### Conformance assertions

An implementation claiming this walkthrough should be able to demonstrate that:

1. recognition alone never grants the requested action when scope or delegation is absent;
2. a revoked authority or delegation cannot produce a positive decision for the affected decision time;
3. stale or conflicting trust state is surfaced explicitly and never silently coerced to `allow`;
4. identical pinned inputs replay to the same governed outcome and reason code; and
5. a correction produces a new decision linked to, rather than overwriting, the historical receipt.

