# HTTP Transport Patterns

## Purpose

v0.8.0 and v0.9.0 introduce transport realism for process-aware verification. The reference HTTP service now demonstrates four patterns:

1. direct authorization lookup
2. direct recognition lookup
3. gateway-mediated authorization lookup
4. end-to-end verification and audit bundle export

## Endpoints

- `POST /trqp/authorization`
- `POST /trqp/recognition`
- `POST /trqp/gateway/authorization`
- `POST /trqp/verify`
- `POST /trqp/audit-bundle`

## Design notes

The transport layer is intentionally simple. The objective is to show how process-aware verification, gateway mediation, and audit export can travel over HTTP without turning the repository into a production API gateway.
