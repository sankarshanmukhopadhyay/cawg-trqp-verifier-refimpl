---
layout: default
title: "Privacy Threat Model"
parent: "Privacy and Personal Information"
nav_order: 7
---

# Privacy Threat Model

| Threat | Example | Control evidence |
|---|---|---|
| Actor enumeration | Repeatedly test whether individuals are recognized | authenticated clients, rate limits, response minimization |
| Relationship inference | Discover label, employer, or delegation links | scoped authorization, minimal reason codes, gateway policy |
| Context injection | Insert sensitive attributes into arbitrary JSON | allow-listed context schema |
| Audit exfiltration | Request raw replay bundles | privileged export scope and access log |
| Cross-tenant cache leakage | Reuse decision across authorities | canonical authority-bound cache keys |
| Pseudonym reversal | Dictionary attack on plain hashes | keyed digests and key governance |
| Registry correlation | Link queries across jurisdictions | routing minimization and retention limits |
| Stale adverse decision | Corrected record not propagated | revocation and cache invalidation tests |

```mermaid
flowchart TB
    A[Untrusted client] --> Q[Query surface]
    Q --> ENUM[Enumeration]
    Q --> INJ[Context injection]
    Q --> EXP[Evidence export abuse]
    G[Gateway] --> CORR[Cross-registry correlation]
    C[Cache] --> LEAK[Cross-tenant leakage]
    E[Evidence store] --> EXF[Exfiltration]
    ENUM & INJ & EXP & CORR & LEAK & EXF --> CTRL[Access, minimization, isolation, retention, monitoring]
```
