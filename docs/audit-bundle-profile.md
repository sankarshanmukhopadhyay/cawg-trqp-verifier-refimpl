# Audit Bundle Profile

## Current profile state

Audit bundles now carry both evidence and the **resolved verification profile** that governed the decision.

The deterministic profile for bundle export includes:

- `request_summary`
- `verification_result`
- `policy_evidence`
- `process_appraisal`
- `gateway_mediation`
- `replay_inputs`
- optional `bundle_attestation`

## v0.12.0 addition

`replay_inputs.profile` now stores the resolved profile object rather than only the profile name. This preserves:

- base profile identity
- active controls
- overlay list
- profile source metadata

## Assurance effect

A replay consumer can now validate not only whether the same inputs produce the same result, but whether they were evaluated under the same governance contract.
