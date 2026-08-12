---
layout: default
title: "Walkthroughs"
nav_order: 9
has_children: true
description: "End-to-end scenarios showing the verifier applied to concrete governance decisions."
---

# Walkthroughs

These scenarios show how content-authenticity evidence and governed authority can be combined without collapsing provenance, authorization, and downstream truth or professional judgment into one decision. The portfolio now also applies a common [Agentic AI Assurance](../agentic-ai/index.md) overlay so an AI agent can be pressure-tested as producer, submitter, verifier, orchestrator, proxy, or decision actor without treating agent identity as authority. Each walkthrough exposes the decision boundary, authority/delegation model, revocation and freshness behavior, failure states, correction lineage, evidence outputs, and replay expectations.

## Start by assurance pattern

| Assurance pattern | Representative walkthroughs | What it pressure-tests |
|---|---|---|
| Publication and public communication | [Breaking-News Photography](../workflows/breaking-news-photography.md), [Video Verification](../video-verification-walkthrough.md), [Political Campaign Advertising](../workflows/political-campaign-advertising.md) | editorial/campaign authority, rapid revocation, conflicting state |
| Rights and commercial authorization | [Authorized Music Distribution](../workflows/authorized-music-distribution.md), [AI-Assisted Property Listing Images](../workflows/property-listing-ai-image-verification.md), [Marketplace Product Images](../workflows/marketplace-product-images.md) | delegated rights, disclosure scope, platform disposition |
| Regulated or evidentiary intake | [Insurance Claim Evidence](../workflows/insurance-claim-evidence.md), [Medical Imaging](../workflows/medical-imaging-remote-consultation.md), [Legal and Administrative Evidence](../workflows/legal-evidence-submission.md) | separation of intake from substantive adjudication |
| Field and operational evidence | [Body-Camera Evidence](../workflows/body-camera-evidence.md), [Construction Milestones](../workflows/construction-milestone-certification.md), [Disaster Response](../workflows/disaster-response-damage-assessment.md), [Industrial Inspection](../workflows/industrial-inspection-maintenance.md) | device/actor delegation, offline or delayed state, safety boundaries |
| Long-lived and correction-sensitive evidence | [Scientific Research Imagery](../workflows/scientific-research-imagery.md), [Cultural Heritage and Archive Ingest](../workflows/cultural-heritage-archive-ingest.md), [Photography Contest](../workflows/photography-contest-verification.md) | reproducibility, immutable correction, preserved historical state |
| Constrained/humanitarian environments | [Humanitarian Offline Field Evidence](../workflows/humanitarian-offline-field-evidence.md), [Warranty and Repair Evidence](../workflows/warranty-repair-evidence.md) | intermittent connectivity, delegated service roles, contested evidence |

## Complete walkthrough portfolio

### Agentic assurance archetypes

- [Agent as Content Producer](../workflows/agent-content-producer.md)
- [Agent as Delegated Submitter](../workflows/agent-delegated-submitter.md)
- [Agent as Verifier and Orchestrator](../workflows/agent-verifier-orchestrator.md)

These cross-sector archetypes define reusable mandate, scope, revocation, tool-chain, replay, and decision-boundary controls. Every sector walkthrough below includes an **Agentic AI Variant** that instantiates the same model in context.


### Foundational and implementation-led examples

- [Photography Contest Verification](../workflows/photography-contest-verification.md)
- [Video Verification Walkthrough](../video-verification-walkthrough.md)
- [Authorized Music Distribution](../workflows/authorized-music-distribution.md)
- [AI-Assisted Property Listing Images](../workflows/property-listing-ai-image-verification.md)

### Cross-sector assurance scenarios

- [Breaking-News Photography](../workflows/breaking-news-photography.md)
- [Insurance Claim Evidence](../workflows/insurance-claim-evidence.md)
- [Marketplace Product Images](../workflows/marketplace-product-images.md)
- [Medical Imaging for Remote Consultation](../workflows/medical-imaging-remote-consultation.md)
- [Body-Camera and Municipal Evidence](../workflows/body-camera-evidence.md)
- [Construction Milestone Certification](../workflows/construction-milestone-certification.md)
- [Humanitarian Offline Field Evidence](../workflows/humanitarian-offline-field-evidence.md)
- [Political Campaign Advertising](../workflows/political-campaign-advertising.md)
- [Warranty and Repair Evidence](../workflows/warranty-repair-evidence.md)
- [Scientific Research Imagery](../workflows/scientific-research-imagery.md)

### New assurance-boundary scenarios

- [Disaster Response Damage Assessment](../workflows/disaster-response-damage-assessment.md)
- [Legal and Administrative Evidence Submission](../workflows/legal-evidence-submission.md)
- [Industrial Inspection and Maintenance Evidence](../workflows/industrial-inspection-maintenance.md)
- [Cultural Heritage and Archive Ingest](../workflows/cultural-heritage-archive-ingest.md)

## Common assurance contract

Across the portfolio, a positive verifier result means only that the requested action satisfies the configured provenance, authority, scope, policy, and trust-state requirements. It does **not** establish factual truth or transfer the relying organization's legal, editorial, clinical, engineering, evidentiary, or policy responsibility to the verifier.

The machine-readable scenario manifests under `examples/*/scenario.json` exercise six common lifecycle states, including the agentic archetypes: authorized, scope mismatch, revoked, stale, conflict, and corrected. CI discovers these manifests dynamically and verifies that they resolve to published walkthrough documents.
