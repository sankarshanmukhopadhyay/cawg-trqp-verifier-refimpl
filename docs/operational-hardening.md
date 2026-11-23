---
layout: default
title: "Operational Hardening"
description: "HTTP boundary hardening and structured audit events."
parent: "Architecture & Deployment"
nav_order: 5
---
# Operational Hardening

## HTTP Boundary

The HTTP service enforces:

- `application/json` request bodies
- bounded request size through Flask `MAX_CONTENT_LENGTH`
- typed verification request fields
- built-in API profile resolution only
- rejection of profile filesystem references

## Structured Audit Events

Verification and audit-bundle HTTP calls emit structured JSON events through the Flask application logger.

Each event includes:

- `event_type`
- `profile`
- `use_gateway`
- `verification_mode`
- `trust_outcome`
- `policy_freshness`

Operators can route these logs into a SIEM, policy audit store, or deployment observability plane.

## Deployment Defaults

Recommended production deployment posture:

| Control | Recommendation |
|---|---|
| TLS | Terminate TLS at a trusted reverse proxy. |
| Request size | Keep the default 64 KiB limit unless a documented fixture requires more. |
| Rate limiting | Apply per-client and per-authority limits at the reverse proxy. |
| Logging | Preserve structured audit logs with immutable retention. |
| Profiles | Expose only built-in profiles and governed overlays through API boundaries. |
| Replay | Require a trusted replay root and pinned digests for bundle-referenced feeds. |

## Release checksum evidence

`release-assets/checksums-v0.16.0.json` is **historical**, not the current release manifest. For current source checkouts, `scripts/generate_release_checksums.py` generates and checks an evidence manifest for selected source inputs; it does not hash the built wheel or sdist. Use `python scripts/generate_release_checksums.py` and `python scripts/generate_release_checksums.py --check` for current-checkout validation. For an immutable published baseline, pin the corresponding tag and use its release-attached checksum artifact, such as [v0.21.0](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/tag/v0.21.0).

## Operational freshness and legacy replay

The HTTP wrapper reuses a long-lived verifier and an in-process decision cache. A known epoch mismatch invalidates cached authority or recognition entries, but does not establish that an external feed update reaches the service automatically. Deployments must separately manage feed refresh, trust-source authentication, fail-closed policy selection and propagation monitoring. Do not present `standard` profile warning outcomes as current-authority assurance when `policy_freshness=stale_but_warned`.

Historical replay bundles with future-issued revocation evidence remain unmodified; the current `make validate` gate checks their known incompatibility rather than claiming that the former freshness assertion still replays as fresh. See the [reproducibility guide](reproducibility-guide.md).
