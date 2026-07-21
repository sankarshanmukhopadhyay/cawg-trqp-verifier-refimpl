---
layout: default
title: "Key Compromise and Recovery"
parent: "Threats and Risks"
nav_order: 90
---

# Key Compromise and Recovery

Keys may protect CAWG assertions, registry responses, feed descriptors, gateway routes, decision receipts, or release artifacts. Compromise must be recoverable without silently preserving attacker-issued trust.

```mermaid
sequenceDiagram
  participant M as Monitor
  participant O as Operator
  participant T as Trust system
  participant C as Cache
  participant E as Evidence store
  M->>O: Key compromise alert
  O->>T: Revoke key and descriptor
  O->>C: Invalidate affected entries
  O->>T: Rotate and publish replacement
  O->>E: Mark affected evidence interval
  O->>T: Replay or re-evaluate decisions
  T-->>O: Recovery report
```

## Recovery requirements

1. Identify key scope and affected time interval.
2. Revoke or distrust the compromised key.
3. Invalidate routes, descriptors, cache entries, and snapshots derived from it.
4. Rotate keys under independent approval.
5. Re-evaluate affected decisions where material.
6. Preserve incident and restoration evidence.
7. Notify relying parties according to deployment policy.
8. Reassess residual risk before resuming normal operation.
