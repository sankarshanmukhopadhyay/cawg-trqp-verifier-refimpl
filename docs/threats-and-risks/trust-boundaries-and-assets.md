---
layout: default
title: "Trust Boundaries and Assets"
parent: "Threats and Risks"
nav_order: 30
---

# Trust Boundaries and Assets

```mermaid
flowchart TB
  subgraph Z0[Zone 0: Untrusted intake]
    U[Uploader] --> M[Media + manifest]
  end
  subgraph Z1[Zone 1: Validation]
    P[Parser] --> C[Cryptographic validation]
  end
  subgraph Z2[Zone 2: Decision plane]
    N[Normalizer] --> V[Verifier]
    V <--> K[(Cache)]
  end
  subgraph Z3[Zone 3: Federation]
    G[Gateway] --> R[Registries]
  end
  subgraph Z4[Zone 4: Evidence and operations]
    E[(Evidence store)]
    A[Administrator / assessor]
  end
  M --> P
  C --> N
  V --> G
  V --> E
  A --> E
  A --> G
```

| Boundary | Data crossing | Required controls | Evidence |
|---|---|---|---|
| Intake → validator | Untrusted binary and assertions | size limits, parser isolation, supported-format policy | validation report |
| Validator → adapter | Validated assertion set | typed extraction, source binding, mapping version | integration signal |
| Adapter → verifier | Actor, issuer, action, resource, context | schema validation, minimization, integrity | request digest |
| Verifier → cache | Decision and policy evidence | canonical keys, tenant isolation, TTL, invalidation | cache provenance |
| Verifier → gateway | Recognition and authorization query | authentication, confidentiality, replay protection | mediation trace |
| Gateway → registry | Routed query | authority pinning, route integrity, timeout budget | route descriptor |
| Verifier → evidence store | Receipt or replay bundle | access control, encryption, retention | bundle digest and profile |
| Operator → control plane | Configuration and override | least privilege, approval, audit, revocation | change record |

Critical assets and their objectives are represented in [`governance/attack-surface.yaml`](../../governance/attack-surface.yaml).
