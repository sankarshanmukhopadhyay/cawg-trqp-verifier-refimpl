---
title: Cache, Freshness, and Revocation
parent: Implementation Guide
nav_order: 71
---

# Cache, freshness, and revocation

Caching is not merely a performance switch. It is an executable governance control balancing bounded staleness, revocation urgency, availability and remote dependency.

## Decision model

Lookup posture should be selected using:

```text
risk × freshness sensitivity × revocation urgency × availability requirement
```

| Mode | Typical use | Required evidence |
|---|---|---|
| Pinned snapshot | Offline and deterministic replay | Signed snapshot, expiry and digest |
| Cache-first | High-volume routine verification | Cache age, policy epoch and source |
| Stale-while-revalidate | Availability-sensitive flows | Stale age, refresh attempt and limit |
| Live-on-risk | Elevated-risk action or context | Risk trigger and live response |
| Live-only | Critical revocation or regulated decision | Current authoritative response |
| Fail-closed | Unacceptable uncertainty | Explicit rejection reason |
| Deferred/indeterminate | Continuity with bounded uncertainty | Uncertainty and retry evidence |

## Cache safety requirements

A conforming deployment should:

- include authority, actor, action, resource and canonical context in the key;
- prevent cache collisions across authorities and jurisdictions;
- bind entries to a policy epoch or authoritative digest where available;
- apply shorter TTLs to negative or high-risk decisions;
- invalidate on relevant revocation deltas;
- record cache provenance in the decision receipt;
- bypass cache when the selected profile requires live evidence;
- bound any stale-while-revalidate interval;
- expose hit, miss, eviction, expiration and refresh metrics.

## HTTP lifecycle correction

The HTTP service uses long-lived verifier instances backed by one thread-safe L1 cache. Cache entries therefore persist across separate HTTP requests. Earlier request-scoped verifier construction discarded the cache after every call and did not realize the documented `standard` cache-first posture.

The in-memory adapter is intentionally replaceable. Multi-process or multi-node deployments require a shared cache or policy-feed distribution strategy if consistent reuse is required across workers.

## Revocation precedence

A fresh cache entry is not sufficient when a newer revocation delta applies. Revocation evaluation precedes authorization reuse in the verifier. Deployments should additionally invalidate affected entries when receiving deltas and retain the delta epoch in evidence.

## Machine-readable policy

`schemas/cache-policy.schema.json` defines portable controls for cache mode, maximum TTL, negative TTL, stale-while-revalidate, policy-epoch requirements, revocation invalidation, risk-triggered live lookup and failure behavior.
