# Verifier Profiles

| Profile | Network | Throughput | Primary TRQP mode |
|---|---|---:|---|
| edge | intermittent | high | snapshot |
| standard | stable | medium | cache-first |
| high_assurance | stable | medium | live lookup |

## Edge

- local integrity verification
- local snapshot lookup
- explicit freshness in output
- deferred handling for missing state

## Standard

- cache-first authorization and recognition
- live lookup on miss
- bounded freshness

## High assurance

- live lookup by policy
- stronger audit posture
- revocation sensitivity
