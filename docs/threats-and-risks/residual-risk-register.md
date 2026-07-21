---
layout: default
title: "Residual Risk Register"
parent: "Threats and Risks"
nav_order: 130
---

# Residual Risk Register

Residual risk is a governed decision, not an undocumented remainder.

```mermaid
flowchart TD
  I[Inherent risk] --> C[Controls]
  C --> T[Tests and evidence]
  T --> R[Residual risk]
  R --> D{Decision}
  D -->|accept| A[Owner + expiry]
  D -->|mitigate| M[Additional controls]
  D -->|transfer| X[Contract / insurance / service]
  D -->|stop| S[Do not deploy]
  A --> Q[Scheduled reassessment]
  M --> T
```

Every accepted risk must state:

- accountable owner;
- decision authority;
- rationale;
- affected scope;
- current controls;
- monitoring indicators;
- acceptance expiry;
- reassessment triggers;
- revocation or stop condition;
- evidence references.

The authoritative machine-readable register is [`governance/residual-risk-register.yaml`](../../governance/residual-risk-register.yaml). Acceptance entries without an owner or expiry fail repository conformance.
