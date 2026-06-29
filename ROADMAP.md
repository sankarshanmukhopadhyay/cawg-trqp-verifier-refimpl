# Roadmap

## Completed through v0.15.0

The reference implementation now provides an executable CAWG-TRQP assurance surface rather than only a verifier demo.

- canonical fixture packages exist for standard, high-assurance, gateway-mediated, and multi-authority verification cases
- transport, revocation, profile, replay, and feed descriptor evidence are exported into verification results and audit bundles
- signed policy, revocation, snapshot, and gateway route feed descriptors are schema-backed and validated at runtime
- high-assurance verification fails closed when required descriptor evidence is missing or invalid
- HTTP verification routes reject malformed input, oversized requests, non-JSON payloads, and unsafe profile path references
- audit replay checks bundle-referenced feed paths against a trusted replay root and validates pinned feed digests before use
- richer freshness and descriptor reason codes are available for stale, missing, degraded, malformed, unverifiable, digest-mismatched, unauthorized, and unattested feed states
- the compatibility matrix and risk-to-test map provide machine-readable evidence for conformance and assurance planning

## Current release posture

v0.15.0 closes the prior signed feed descriptor and transport-attestation roadmap item and converts the most security-sensitive trust boundaries into tested controls.

The repository intentionally preserves the JSON fixture and C2PA-style manifest-store paths. It does not claim full binary C2PA manifest extraction. That higher-fidelity parser should be added through an adapter boundary so that the trust-signal contract remains stable while ecosystem-specific extraction libraries evolve.

## Next practical increments

### 1. External assurance-suite ingestion

- publish fixture manifests in a form that an external TRQP conformance suite can ingest directly
- add implementation identity and replay-result attestations for third-party implementations
- map compatibility claims to assurance levels and negative-vector classes

### 2. Binary CAWG/C2PA parser adapter

- preserve the current JSON fixture path
- add a parser adapter interface for real C2PA extraction libraries
- add binary fixture samples only when redistribution rights and deterministic validation are clear
- keep actor, issuer, assertion, process, provenance, and integrity signals stable across parser backends

### 3. Descriptor policy configuration

- expose descriptor enforcement as a profile-level policy for each feed type
- support observe, warn, and fail semantics for policy, revocation, snapshot, and gateway descriptors
- add route-specific gateway attestation vectors

### 4. Operational hardening

- add structured audit logs for HTTP deployments
- publish deployment defaults for reverse-proxy, TLS, rate limiting, and request-size policy
- add signed release-asset checksums for archive distribution
