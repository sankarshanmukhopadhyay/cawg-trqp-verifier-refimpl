# Verifier Profiles

- `edge`: snapshot-based offline verification
- `standard`: cache-first online verification
- `high_assurance`: always-live policy lookups

Gateway mediation can be layered on top of standard or high assurance operation.

## Deterministic export note

When verification results are exported as audit bundles, the selected profile is copied into `replay_inputs.profile` so downstream systems can replay the same operating mode explicitly instead of inferring it from surrounding context.
