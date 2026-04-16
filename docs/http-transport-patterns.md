# HTTP Transport Patterns

The repository exposes a Flask-based HTTP service for authorization, recognition, verification, and audit bundle export.

## Why the HTTP surface matters

The codebase is not only a library. It is also an executable reference for how a verifier can expose TRQP-adjacent policy and evidence operations over a network boundary.

## Included endpoints

- `GET /health`
- `POST /trqp/authorization`
- `POST /trqp/recognition`
- `POST /trqp/gateway/authorization`
- `POST /trqp/verify`
- `POST /trqp/audit-bundle`

## Testing posture

The repository now covers this surface in two ways:

- Flask test-client tests for endpoint behavior
- an integration test that starts the real service process and verifies the live `/health` and `/trqp/verify` paths

This matters because a deployment claim is stronger when both the application surface and the process startup path are exercised.
