# Architecture

## Release focus

In `v0.13.0`, the verifier moves from profile-governed policy execution to **profile-governed input trust plus replay fidelity**.

The architecture now treats transport posture and revocation freshness as part of the same control surface as authorization, recognition, and process appraisal.

## Main flow

1. Load a request from JSON or fixture.
2. Resolve the verification profile and any overlays.
3. Evaluate transport constraints against the active service or gateway path.
4. Evaluate revocation freshness against the profile contract.
5. Execute authorization and recognition lookups when permitted.
6. Appraise process evidence against policy requirements.
7. Export result, policy evidence, and replay inputs.

## Control surfaces

### Verification profile

The profile remains the governing unit. In `v0.13.0`, it now includes:

- authority controls
- freshness controls
- revocation controls
- failure behavior
- evidence behavior
- transport requirements
- determinism expectations

### Transport evaluation

The verifier records:

- required transport posture from the profile
- actual transport posture from the runtime path
- whether the transport contract was satisfied
- any transport violations

### Revocation freshness evaluation

The verifier records:

- revocation source and channel
- age of revocation material when available
- max allowed age from the profile
- whether the freshness contract was satisfied
- any freshness violations

## Export path

Audit bundles now carry richer replay inputs so downstream systems can test not just the result, but also whether the same input trust conditions were asserted.

## Architectural implication

This is a meaningful control-plane shift.

The system is no longer only saying, “here is the answer.” It is saying, “here is the answer, here is what I required from my inputs, and here is whether those requirements were actually met.”
