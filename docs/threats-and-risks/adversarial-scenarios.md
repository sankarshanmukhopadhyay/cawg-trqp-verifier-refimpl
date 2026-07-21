---
layout: default
title: "Adversarial Scenarios"
parent: "Threats and Risks"
nav_order: 50
---

# Adversarial Scenarios

The canonical scenarios are represented as YAML examples under [`examples/threats/`](../../examples/threats/). Each scenario identifies preconditions, attack path, impact, controls, evidence, tests, and residual risk.

## Gateway route substitution

```mermaid
sequenceDiagram
    participant A as Attacker
    participant G as Gateway
    participant V as Verifier
    participant R as Rogue registry
    participant C as Cache
    A->>G: Replace authority route
    V->>G: Authorization query
    G->>R: Forward to rogue registry
    R-->>G: Syntactically valid approval
    G-->>V: Approval + manipulated trace
    V->>C: Cache poisoned decision
    V-->>V: Issue apparently valid receipt
```

Required controls include signed route descriptors, route-authority pinning, route evidence in receipts, cache invalidation, and route-key revocation.

## Registry equivocation

```mermaid
flowchart LR
    R[Registry] -->|approved| V1[Verifier A]
    R -->|revoked| V2[Verifier B]
    V1 --> O[Observer comparison]
    V2 --> O
    O -->|digest mismatch| X[Equivocation alert]
```

## Cache poisoning and stale extension

```mermaid
stateDiagram-v2
    [*] --> Miss
    Miss --> LiveLookup
    LiveLookup --> VerifiedEntry
    VerifiedEntry --> Hit
    Hit --> Expired
    Expired --> LiveLookup
    VerifiedEntry --> Quarantined: epoch/revocation mismatch
    Quarantined --> Invalidated
```

## Parser resource exhaustion

Controls must bound input size, parsing time, nesting, decompression ratio, and unsupported-format behavior before policy evaluation begins.

## Governance policy capture

A technically valid policy update can still be abusive. Material recognition, exclusion, override, and revocation changes require documented authority, review, evidence, effective period, appeal, and reassessment.
