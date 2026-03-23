# Verifier Profiles

| Profile | Network | Throughput | Primary TRQP mode | Process posture |
|---|---|---:|---|---|
| edge | intermittent | high | snapshot | local appraisal against snapshot-backed policy requirements |
| standard | stable | medium | cache-first | policy-aware synthesis with cache reuse |
| high_assurance | stable | medium | live lookup | strict live policy evaluation plus process requirement enforcement |

## Edge

- local integrity verification
- local snapshot lookup
- explicit freshness in output
- local process appraisal from supplied evidence
- deferred or rejected handling for missing state or missing required process proof

## Standard

- cache-first authorization and recognition
- live lookup on miss
- bounded freshness
- process-aware synthesis using policy requirements carried in authorization responses

## High assurance

- live lookup by policy
- stronger audit posture
- revocation sensitivity
- strict process requirement enforcement with no cache bypass
