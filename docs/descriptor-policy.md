---
layout: default
title: "Descriptor Policy"
description: "Profile-level observe/warn/fail semantics for feed descriptor enforcement."
parent: "Implementation Guides"
nav_order: 3
---
# Descriptor Policy

## Purpose

v0.16.0 makes feed descriptor enforcement explicit at profile level. This removes ambiguity between observing descriptor evidence and failing closed when descriptor trust is mandatory.

The profile control is:

```json
"descriptor_policy": {
  "policy": "observe",
  "revocation": "observe",
  "snapshot": "observe",
  "gateway_route": "observe"
}
```

Each feed type supports:

| Mode | Runtime meaning |
|---|---|
| `observe` | Emit descriptor evidence without changing the decision. |
| `warn` | Preserve descriptor evidence for operator review and audit. |
| `fail` | Treat descriptor validation failure as a verification failure. |

## Built-In Profiles

| Profile | Policy | Revocation | Snapshot | Gateway Route |
|---|---:|---:|---:|---:|
| `standard` | `observe` | `observe` | `observe` | `observe` |
| `edge` | `observe` | `observe` | `fail` | `observe` |
| `high_assurance` | `fail` | `fail` | `warn` | `fail` |

## Evidence Surface

Runtime descriptor evidence is emitted under:

- `policy_evidence.feed_descriptors`
- `replay_inputs.feed_descriptors`

Important reason codes include:

- `fresh`
- `missing_feed_descriptor`
- `descriptor_malformed`
- `descriptor_signature_invalid`
- `descriptor_digest_mismatch`
- `authority_not_recognized`
- `route_unattested`
- `stale_rejected`

## Assurance Rule

High-assurance verification must provide valid policy and revocation feed descriptors. Missing descriptors remain a tested fail-closed condition.
