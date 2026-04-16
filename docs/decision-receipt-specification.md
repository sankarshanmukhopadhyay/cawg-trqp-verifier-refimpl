---
title: Decision Receipt Specification
description: Defines the structure, semantics, and lifecycle of replayable trust decisions produced by the verifier.
---

# Decision Receipt Specification

This document defines the structure and semantics of a **decision receipt**.

A decision receipt is a machine-verifiable artifact that captures:

- what decision was made
- what authority was relied upon
- what policy was applied
- what inputs were evaluated
- what result was produced

It enables:

- audit
- replay
- dispute resolution
- cross-system verification

---

# Why decision receipts exist

Most systems produce decisions without preserving:

- the authority context used
- the policy conditions applied
- the inputs evaluated at the time

This makes decisions:

- non-reproducible
- non-auditable
- difficult to challenge or validate

Decision receipts solve this by making every decision:

> reconstructable, inspectable, and replayable

---

# Core properties

A valid decision receipt must be:

## Deterministic
Replaying the receipt must produce the same result.

## Complete
All required inputs, responses, and conditions must be included.

## Verifiable
The receipt must be independently checkable.

## Portable
The receipt must be usable across systems.

## Tamper-evident
Any modification must be detectable.

---

# Receipt structure

A decision receipt is a structured JSON document.

## Top-level structure

```json
{
  "receipt_version": "1.0",
  "receipt_id": "uuid",
  "timestamp": "ISO8601",
  "profile": "standard | high_assurance | edge",
  "verification_mode": "online_full | gateway | offline_snapshot",
  "transport_mode": "direct | gateway | snapshot",

  "input": { ... },
  "trqp_responses": { ... },
  "policy_evaluation": { ... },
  "decision": { ... },
  "evidence": { ... }
}
```

---

# Section breakdown

## 1. Input

Describes what was evaluated.

```json
"input": {
  "asset": {
    "type": "video",
    "id": "city-bridge-inspection.mp4",
    "hash": "sha256-..."
  },
  "actor": {
    "id": "did:example:vendor123"
  },
  "issuer": {
    "id": "did:example:issuer456"
  },
  "authority": {
    "id": "city.infrastructure.authority"
  },
  "action": "submit_inspection_video",
  "signals": {
    "integrity": "verified",
    "provenance": "present",
    "process_evidence": "declared"
  }
}
```

---

## 2. TRQP responses

Captures the exact responses returned by the trust registry.

```json
"trqp_responses": {
  "authorization": {
    "result": "allowed",
    "source": "authority-A",
    "timestamp": "..."
  },
  "recognition": {
    "result": "recognized",
    "source": "authority-B",
    "timestamp": "..."
  },
  "revocation": {
    "status": "active",
    "checked_at": "...",
    "freshness_seconds": 120
  }
}
```

These must be:

- complete
- timestamped
- attributable to a source

---

## 3. Policy evaluation

Describes how the system interpreted inputs and responses.

```json
"policy_evaluation": {
  "profile_rules_applied": [
    "require_fresh_revocation",
    "require_trusted_transport"
  ],
  "checks": {
    "authorization": "pass",
    "recognition": "pass",
    "revocation_freshness": "pass",
    "integrity": "pass",
    "process_evidence": "pass"
  }
}
```

This section bridges:

- raw TRQP responses  
- final decision logic  

---

## 4. Decision

The final outcome.

```json
"decision": {
  "result": "trusted",
  "confidence": "high",
  "reasons": [
    "authorized_actor",
    "recognized_issuer",
    "fresh_revocation",
    "valid_process"
  ]
}
```

Possible values:
- trusted
- rejected
- degraded

---

## 5. Evidence

Supports replay and audit.

```json
"evidence": {
  "replayable": true,
  "snapshot_reference": "snapshot-2026-04-16",
  "gateway_route": "route-A",
  "logs_hash": "sha256-...",
  "signature": "..."
}
```

This may include:

- signed snapshots
- gateway metadata
- integrity hashes
- signatures

---

# Replay model

A receipt must support deterministic replay.

Replay process:

1. Load receipt
2. Reconstruct input
3. Reuse TRQP responses (or validate against snapshot)
4. Apply policy evaluation
5. recompute decision
6. compare outputs

If outputs differ:

- the receipt is invalid  
- or the system has changed  

---

# Receipt validation rules

A valid receipt must:

- include all required sections
- contain consistent timestamps
- include verifiable TRQP sources
- match profile constraints
- produce identical replay results

---

# Profiles and receipts

Profiles directly affect receipts.

## Standard
- allows normal freshness and transport
- receipt reflects operational conditions

## High assurance
- stricter constraints
- receipt must show stronger guarantees

## Edge
- snapshot-based
- receipt must include snapshot verification data

---

# Transport traceability

Receipts must capture transport context:

- direct queries
- gateway routing
- snapshot usage

This ensures:

- decisions can be traced to their data sources  
- mediation layers are visible  

---

# Multi-authority receipts

Receipts may include multiple authority contexts:

```json
"trqp_responses": {
  "authorization": { "source": "authority-A" },
  "recognition": { "source": "authority-B" }
}
```

The receipt must clearly show:

- which authority contributed which decision  
- how they were combined  

---

# Relationship to ecosystem

Decision receipts integrate with:

- TRQP Hub → defines expected controls
- Conformance Suite → validates receipt correctness
- TSPP → constrains acceptable providers
- Verifier → produces receipts

---

# Minimal conformance profile

A conformant implementation must:

- produce receipts for every decision
- include all required sections
- support replay
- validate receipt integrity

---

# Future extensions

Possible extensions include:

- cryptographic signing standards
- standardized receipt schemas across ecosystems
- dispute workflows and challenge protocols
- receipt aggregation across decision chains

---

# Summary

Decision receipts transform trust decisions from:

- opaque outcomes  
- implicit authority  
- non-reproducible logic  

Into:

- explicit authority usage  
- structured policy evaluation  
- replayable, auditable evidence  

They are the foundation for making trust decisions **verifiable in operation**.
