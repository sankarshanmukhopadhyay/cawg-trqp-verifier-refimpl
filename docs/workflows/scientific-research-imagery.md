---
layout: default
title: "Scientific Research Imagery"
parent: "Walkthroughs"
nav_order: 19
description: "Real-world CAWG-TRQP governance walkthrough."
---
# Scientific Research Imagery

## Purpose and decision boundary

A laboratory submits instrument-generated imagery for a dataset or publication. The verifier records laboratory, operator, instrument, processing history, and correction or retraction status.

The decision is deliberately narrow:

> **May this asset be used for research dataset or publication under the authority, scope, policy, and trust state recorded at decision time?**

A successful result does not establish factual truth, legal liability, professional judgment, product authenticity, clinical validity, or entitlement beyond that scoped action.

## At-a-glance governance flow

```mermaid
flowchart LR
    A[Researcher submits instrument imagery] --> B[Repository validates provenance and processing history]
    B --> C[Verifier checks laboratory operator instrument and study scope]
    C --> D{Dataset or publication use authorized?}
    D -- Yes --> E[Admit with declared transformations]
    D -- No --> F[Reject or request corrected metadata]
    D -- Conflict or retraction --> G[Quarantine and review]
    E --> H[Issue receipt and preserve version lineage]
    F --> H
    G --> H
```

The decision establishes governed origin and permitted use; it does not independently validate the scientific conclusion.

## Actors and authority

| Role | Responsibility | Evidence expected |
|---|---|---|
| Submitter | Supplies the asset and declared context | CAWG/C2PA-derived integration signal |
| Governing authority | Defines who may perform `admit_research_asset` | Signed policy and recognition information |
| Relying service | Applies the decision to its own workflow | Decision receipt and reason codes |
| Affected party | May challenge metadata, authority, or use | Correction, appeal, or redress reference |
| Assurance reviewer | Replays and audits the decision | Pinned inputs and audit bundle |

## Governance concerns

- **Instrument Provenance:** represented as explicit policy, context, evidence, or review requirements.
- **Laboratory Authority:** represented as explicit policy, context, evidence, or review requirements.
- **Processing Declaration:** represented as explicit policy, context, evidence, or review requirements.
- **Retraction And Versioning:** represented as explicit policy, context, evidence, or review requirements.

## End-to-end sequence

1. Validate the content-authenticity input and normalize it into the CAWG-TRQP integration signal.
2. Resolve the actor, `research-institution` authority source, and relevant delegation chain.
3. Evaluate `admit_research_asset` against asset, resource, jurisdiction, purpose, and time scope.
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

The companion directory [`examples/scientific-research-imagery/`](../../examples/scientific-research-imagery/README.md) contains a machine-readable scenario manifest and expected outcomes. Run:

```bash
python scripts/validate_walkthrough_examples.py
```

## Evidence produced

- scoped decision and stable reason codes;
- authority, delegation, and revocation evidence references;
- policy and context-profile versions;
- minimized decision receipt;
- replay inputs and correction lineage; and
- an explicit review or redress route for contested decisions.

## What this walkthrough does not prove

This walkthrough does not convert provenance into truth and does not transfer institutional accountability to the verifier. The relying organization remains responsible for the lawful, proportionate, and procedurally fair use of the result.
