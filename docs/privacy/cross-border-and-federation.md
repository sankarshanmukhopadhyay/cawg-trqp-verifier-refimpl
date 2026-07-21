---
layout: default
title: "Cross-Border and Federation"
parent: "Privacy and Personal Information"
nav_order: 6
---

# Cross-Border and Federation

Federated routing can disclose actor, action, resource, and context information to multiple authorities. A gateway must therefore treat route selection as a data-disclosure decision.

```mermaid
flowchart LR
    V[Verifier in jurisdiction A] --> G[Gateway]
    G --> R1[Registry in jurisdiction A]
    G --> R2[Registry in jurisdiction B]
    G --> R3[Registry in jurisdiction C]
    G --> L[Transfer and mediation log]
    L --> P[Approved purpose, destination, safeguards, retention]
```

## Required controls

- route only to authorities necessary for the query;
- document destination, purpose, data categories, and retention;
- prevent exploratory broadcast queries across all registries;
- minimize mediation traces;
- apply contractual, legal, and technical safeguards appropriate to the deployment;
- permit jurisdiction-specific profiles and registry exclusions;
- avoid assuming that federation automatically authorizes international transfer.
