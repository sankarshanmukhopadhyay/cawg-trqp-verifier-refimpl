# Canonical fixtures

This directory packages profile-bound replay fixtures for cross-implementation exchange.

## Included packages

- `standard-v1` — baseline cached-online verification under the standard profile
- `high-assurance-v1` — live-only verification under the high assurance profile
- `gateway-standard-v1` — gateway-mediated verification under the standard profile
- `multi-authority-v1` — gateway-mediated verification with deterministic route selection across multiple authorities

## Package contract

Every fixture package includes:

- `request.json` — verification request to replay
- `resolved_profile.json` — fully resolved executable profile
- `expected_result.json` — expected verification result surface
- `manifest.json` — package metadata, replay contract, and transport expectations
- `pinned_feeds/` — policy and revocation materials used to make the result reproducible

These packages are designed to be exchanged with downstream assurance suites or other implementations without requiring access to the full repository.
