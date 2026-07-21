---
layout: default
title: "Supply Chain and Build Security"
parent: "Threats and Risks"
nav_order: 70
---

# Supply Chain and Build Security

```mermaid
flowchart LR
  S[Source] --> CI[CI workflow]
  D[Dependencies] --> CI
  CI --> T[Tests]
  T --> A[Build artifact]
  A --> SB[Checksums / attestations]
  SB --> P[Published package or image]
  P --> V[Deployment verification]
```

## Required controls

- pin and review dependencies;
- minimize CI permissions;
- protect branches and release workflows;
- generate reproducible checksums and provenance;
- scan packages and container images;
- separate build and signing authority;
- rotate and revoke compromised credentials;
- verify artifacts before deployment;
- preserve test, commit, and environment evidence.

## Compromise response

```mermaid
stateDiagram-v2
  [*] --> Detected
  Detected --> Contain
  Contain --> Revoke
  Revoke --> Rebuild
  Rebuild --> Reverify
  Reverify --> Republish
  Republish --> Notify
  Notify --> [*]
```

A release artifact must never be trusted only because it was obtained from the expected repository location.
