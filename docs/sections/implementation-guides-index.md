---
layout: default
title: "Implementation Guides"
nav_order: 6
has_children: true
description: "How to integrate, operate, evidence, replay, correct, and govern verifier decisions."
---

# Implementation Guides

This section is for teams integrating the verifier into a relying system. It covers integration patterns, verification profiles, descriptor and freshness policy, the parser adapter boundary, the HTTP service contract, audit evidence, replay, correction, and operational redress.

## Recommended adoption path

Use the guides as a progressive implementation journey rather than isolated references:

1. **[Integration Guide](../INTEGRATION_GUIDE.md)** — choose the integration boundary and understand the core verifier contract.
2. **[CAWG Input Contract](../cawg-input-contract.md)** — map provenance/assertion evidence into the verifier without collapsing provenance into authorization.
3. **[API Call Catalogue](../api-call-catalogue.md)** — implement the network contract and explicit failure semantics.
4. **[HTTP to Audit Bundle Adoption Journey](../http-to-audit-bundle-adoption-journey.md)** — run a production-style request through governed verification, evidence export, validation, and deterministic replay.
5. **[Operational Failure, Correction, and Redress](../operational-failure-correction-redress.md)** — exercise revocation, stale evidence, authority conflict, correction, challenge, and incident closure.
6. **[Operator Decision and Replay Walkthrough](../operator-decision-replay-walkthrough.md)** — inspect decision evidence and replay semantics from an operator/auditor perspective.

The executable adoption journey is also represented in `examples/adoption-journeys/http-to-audit-bundle.json`. CI runs `python scripts/validate_adoption_journeys.py` so the published journey must continue to resolve to live OpenAPI endpoints, repository files, commands, and evidence surfaces.

## Adoption completion criteria

An adopter should be able to demonstrate more than a successful API call. The minimum evidence chain is:

```text
bounded request
  -> governed decision
  -> explicit negative/uncertain states
  -> portable audit evidence
  -> independent validation
  -> deterministic replay
  -> correction / supersession
  -> challenge or incident disposition
```

The relying organization remains authoritative for the substantive downstream decision. The verifier provides executable evidence about provenance, authority, scope, policy, and trust state; it does not decide truth, liability, admissibility, clinical validity, entitlement, or remedy.
