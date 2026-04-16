# Architecture

## Current architectural focus

The verifier now treats transport posture, revocation freshness, replay fidelity, fixture exchange, and deployment surfaces as part of one control plane.

That matters because a trust decision is only as credible as the evidence the system can produce about the conditions under which that decision was made.

## Main flow

1. Load a verification request from JSON or a manifest-derived fixture.
2. Resolve the verification profile and any overlays.
3. Evaluate transport constraints against the active service or gateway path.
4. Evaluate revocation freshness against the profile contract.
5. Execute authorization and recognition lookups when permitted.
6. Appraise process evidence against policy requirements.
7. Produce a verification result with policy evidence.
8. Optionally export an audit bundle or compare the result against a canonical fixture.

## Core control surfaces

### Verification profile

The profile remains the governing unit. It contains authority, freshness, revocation, failure, evidence, transport, and determinism controls.

### Transport evaluation

The verifier records the required transport posture from the profile, the actual runtime posture, and any violations. This allows a downstream reviewer to distinguish between a valid decision and a decision reached under a degraded feed path.

### Revocation freshness evaluation

The verifier records the source, channel, age, maximum allowed age, enforcement mode, and any violations. This makes revocation handling inspectable rather than implicit.

### Gateway mediation

When a trust gateway is used, the mediation layer becomes visible evidence. Route labels, target authority identifiers, and mediated recognition behavior become part of the decision surface rather than disappearing into infrastructure.

### Replay and fixture exchange

Replay is no longer limited to rerunning a request. The repository now publishes canonical fixture packages and a compatibility matrix so that another implementation can preserve the same decision semantics and prove what it covered.

## Deployment surfaces

The repository supports four deployment shapes:

- direct verifier invocation against a policy service
- gateway-mediated verification
- offline verification against a signed snapshot
- HTTP service deployment for authorization, recognition, verification, and audit export

## Architectural implication

The repository is now closer to a reusable trust governance substrate.

It does not only answer, “what decision was made?” It answers, “what decision was made, what transport and freshness assumptions were accepted, how was mediation handled, and how can another implementation prove semantic alignment?”
