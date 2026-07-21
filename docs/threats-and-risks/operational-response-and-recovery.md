---
layout: default
title: "Operational Response and Recovery"
parent: "Threats and Risks"
nav_order: 120
---

# Operational Response and Recovery

```mermaid
flowchart LR
  D[Detect] --> T[Triage]
  T --> C[Contain]
  C --> R[Revoke / invalidate]
  R --> E[Eradicate]
  E --> V[Verify recovery]
  V --> N[Notify and restore]
  N --> L[Lessons and reassessment]
  L --> D
```

## Response evidence

| Stage | Required evidence |
|---|---|
| Detect | alert, timestamp, source, affected component |
| Triage | threat ID, scope, severity, decision authority |
| Contain | blocked clients, disabled routes, quarantined evidence |
| Revoke | keys, credentials, cache entries, descriptors, policies |
| Recover | rebuilt artifacts, replay results, control verification |
| Restore | approval, residual-risk decision, communications |
| Learn | root cause, control changes, test additions, expiry |

## Decision authority

Emergency overrides must identify who authorized them, their scope, effective time, expiry, evidence, and revocation path. An override that cannot be revoked is not an acceptable governance control.
