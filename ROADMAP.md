# Roadmap

## Completed after v0.13.0

The adoption and interoperability hardening increment is now in place:

- canonical fixture packages now exist for standard, high assurance, gateway-mediated, and multi-authority cases
- a machine-readable compatibility matrix is published under `conformance/compatibility-matrix.json`
- the HTTP service surface is tested both through endpoint tests and a live-process integration path
- CI uses a pinned validation dependency set and continues to validate shipped examples and fixtures
- documentation now treats the repository as an external handoff surface rather than only as an implementation exercise

## Current focus after the interoperability increment

The next practical work should deepen trust evidence and external alignment.

### 1. Signed feed descriptors and transport attestation

- bind remote feed metadata to signed descriptors
- let gateways attest to upstream route integrity and freshness provenance
- make transport evidence portable outside this implementation

### 2. Richer freshness reason codes

- distinguish stale, missing, degraded, and unverifiable states in a normalized way
- tighten the verification-result schema around exported freshness semantics
- expand negative vectors around degraded and partially trusted freshness states

### 3. External suite integration

- align fixture metadata with broader TRQP conformance work
- let downstream assurance hubs ingest the compatibility matrix directly
- add compatibility statements for independent implementations that replay these packages successfully

### 4. Higher-fidelity CAWG/C2PA parsing

- preserve the current JSON fixture path
- add a path for real binary manifest parsing and extraction
- keep trust-signal extraction stable while increasing ecosystem fidelity
