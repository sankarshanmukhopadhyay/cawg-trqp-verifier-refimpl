---
layout: default
title: "Denial of Service and Scale Abuse"
parent: "Threats and Risks"
nav_order: 80
---

# Denial of Service and Scale Abuse

High-volume claims and cache behavior create adversarial opportunities. An attacker may intentionally force cold lookups, expensive parsing, gateway fan-out, cache eviction, or audit-bundle generation.

```mermaid
flowchart LR
  A[Attack traffic] --> B{Cost amplifier}
  B --> P[Parser CPU / memory]
  B --> C[Cache bypass]
  B --> G[Gateway fan-out]
  B --> R[Registry timeouts]
  B --> E[Evidence serialization]
  P --> O[Overload policy]
  C --> O
  G --> O
  R --> O
  E --> O
  O -->|bounded| D[Degraded / rejected]
  O -->|unbounded| F[Service failure]
```

## Required controls

- per-client and per-authority rate limits;
- bounded request size and parsing budgets;
- cache-key cardinality controls;
- single-flight request coalescing;
- circuit breakers and registry timeout budgets;
- maximum gateway fan-out;
- separate privilege and quotas for audit export;
- queue depth, saturation, and error-rate telemetry;
- explicit fail-closed, indeterminate, or deferred behavior.

Performance evidence must report cache-hit ratio, live-query rate, latency percentiles, errors, and tested environment. See [Scalability and Performance](../scalability-and-performance.md).
