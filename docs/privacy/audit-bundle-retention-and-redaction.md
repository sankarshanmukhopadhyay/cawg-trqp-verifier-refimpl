---
layout: default
title: "Audit Bundle Retention and Redaction"
parent: "Privacy and Personal Information"
nav_order: 4
---

# Audit Bundle Retention and Redaction

The implementation now separates three evidence postures.

| Profile | Default content | Access requirement | Intended use |
|---|---|---|---|
| `minimal_receipt` | Digested identifiers and decision metadata | `trqp.receipt.read` | Routine operational decision |
| `replay_bundle` | Raw request and process evidence | `trqp.audit.export` | Bounded dispute replay |
| `regulated_evidence` | Full controlled evidence | `trqp.audit.regulated` | Documented legal or regulatory obligation |

```mermaid
flowchart TB
    D[Verification decision] --> M[Minimal receipt]
    D --> R{Privileged replay required?}
    R -- No --> M
    R -- Yes --> B[Replay bundle]
    B --> E[Encrypted controlled evidence store]
    E --> T[Retention timer or legal hold]
    T --> X[Delete, anonymize, or retain under authority]
```

The `/trqp/audit-bundle` endpoint defaults to `minimal_receipt`. Raw replay profiles require an `X-TRQP-Scopes` header containing the profile's access scope. This is a reference authorization pattern, not a production identity system.

Retention must be configured per artifact. See `schemas/retention-policy.schema.json` and `examples/privacy/retention-policy.json`.

## Machine-readable evidence governance

Each privacy profile now declares `sensitivity_class`, `retention_class`, `redaction_mode`, and `disclosure_audience`. Audit bundles carry those fields beside the retention period and access scope, so replayability does not require consumers to infer whether an evidence package is safe to retain or disclose. These classifications are reference-implementation governance metadata, not upstream CAWG/C2PA/TRQP semantics.
