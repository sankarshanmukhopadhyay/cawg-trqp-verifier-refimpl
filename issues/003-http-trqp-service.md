# Issue 003: Add HTTP TRQP Service

**Status:** closed in v0.16.0  
**Resolution:** HTTP service exists, is hardened, and emits structured audit events

## Outcome

The HTTP service exposes authorization, recognition, gateway authorization, verification, and audit-bundle routes. It rejects malformed input, non-JSON payloads, oversized requests, and unsafe profile references.

v0.16.0 adds structured HTTP audit events for verification and audit-bundle calls.

## Evidence

- `src/cawg_trqp_refimpl/http_service.py`
- `scripts/start_http_service.py`
- `tests/test_http_service.py`
- `tests/test_http_service_integration.py`
- `tests/test_security_hardening.py`
- `docs/operational-hardening.md`
