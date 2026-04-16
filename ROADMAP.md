# Roadmap

## Completed in v0.13.0

The roadmap direction called out after `v0.12.0` has now been implemented:

- feed transport specialization is now expressed in the profile model and enforced at runtime
- revocation freshness assertions are now explicit and exported in evidence
- cross-implementation fixture exchange now has a canonical package surface
- initial alignment material for broader TRQP assurance and conformance work is now documented

## Current focus after v0.13.0

The next practical increment should deepen evidence about distribution trust and interoperability scale.

### 1. Signed feed descriptors and stronger transport attestation

- bind remote feed metadata to signed descriptors
- express gateway assertions about upstream route integrity
- make transport evidence more portable across implementations

### 2. Richer freshness reason codes

- distinguish stale, missing, degraded, and unverifiable revocation states
- export normalized freshness reason codes in verification results and audit bundles
- add more negative fixtures for degraded freshness scenarios

### 3. Broader fixture exchange coverage

- add canonical fixture packages for `high_assurance`
- add gateway-mediated and multi-authority fixture exchange cases
- define expected negative outcomes for transport and freshness failures

### 4. External suite integration

- align fixture metadata with broader TRQP conformance work
- add compatibility notes for downstream assurance hubs
- publish a minimal machine-readable compatibility matrix
