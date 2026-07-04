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

## Release Checksums

v0.16.0 adds:

- `release-assets/checksums-v0.16.0.json`
- `scripts/generate_release_checksums.py`

Regenerate checksums:

```bash
python scripts/generate_release_checksums.py
```

Validate committed checksums:

```bash
python scripts/generate_release_checksums.py --check
```
