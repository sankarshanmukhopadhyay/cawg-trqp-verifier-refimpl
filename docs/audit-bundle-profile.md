# Audit Bundle Profile

## Purpose

This profile turns verifier output into a portable assurance artifact that can be validated, transferred, replayed, and compared across systems.

## Serialization contract

Bundle fields that are now considered part of the deterministic profile:

- `bundle_type`
- `bundle_profile`
- `bundle_version`
- `exported_at`
- `bundle_id`
- `bundle_digest_sha256`
- `request_summary`
- `verification_result`
- `policy_evidence`
- `process_appraisal`
- `gateway_mediation`
- `replay_inputs`

## Determinism rules

### Canonical digest

`bundle_digest_sha256` is computed over canonical JSON serialization of the bundle content excluding the digest field itself.

### Stable identifier

`bundle_id` uses the following form:

```text
urn:trqp:audit-bundle:sha256:<digest>
```

This lets external systems pin a specific artifact without depending on local filenames or transport metadata.

### Replay material

`replay_inputs` carries the minimum machine-usable information needed to reconstruct the verification request and rerun the decision path.

## Validation workflow

```bash
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.json
```

Validation checks:

1. schema conformance
2. digest correctness
3. identifier format constraints

## Replay workflow

```bash
python scripts/replay_audit_bundle.py \
  examples/exported_audit_bundle.json \
  --policies data/policies.json \
  --revocations data/revocations.json
```

Replay compares the expected and replayed values for core trust decision fields, including:

- asset integrity
- assertion binding
- issuer recognition
- actor authorization
- process integrity
- policy freshness
- verification mode
- trust outcome
- policy epoch

## Scope note

This profile does not yet sign audit bundles directly. The current guarantee is deterministic structure plus digest validation, not independent bundle attestation.


## Optional attestation

Audit bundles may include a `bundle_attestation` object with the following fields:

- `algorithm`: currently `Ed25519`
- `key_id`: trust-anchor key identifier
- `value`: base64-encoded signature over the canonical bundle payload excluding `bundle_attestation`

## Policy feed pinning

`replay_inputs.policy_feed` may include:

- `policy_source`
- `policy_source_sha256`
- `revocation_source`
- `revocation_source_sha256`

These fields allow replay tooling to target the same externalized policy inputs that were used when the bundle was exported.
