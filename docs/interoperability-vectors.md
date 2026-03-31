# Interoperability Vectors

## Current scope

The repository now covers two interoperability layers:

1. **single-authority gateway mediation** for remote policy lookup
2. **multi-authority gateway routing** for production-style federation patterns

## Multi-authority routing model

The trust gateway can route by `authority_id` to distinct policy services and assign a deterministic `route_label` per authority.

This models an execution environment in which:

- different registries govern different content classes or geographies
- the verifier uses one mediation layer
- routing remains explicit and auditable

## Included fixtures

### Policy data

- `data/policies_multi_authority.json`

### Vectors

- `examples/interoperability_vector_gateway.json`
- `examples/interoperability_vector_multi_authority.json`

## Why this matters

A verifier that only supports one authority path is useful for demos but weak for real deployment planning. Multi-authority routing begins to model the actual governance topology of production trust infrastructure.

This improves three properties:

- **scope clarity**: each authority remains distinct
- **auditability**: the mediation record shows which route was used
- **determinism**: route selection is policy-domain driven, not implicit or ad hoc

## Test coverage

Route-aware behavior is exercised in:

- `tests/test_gateway_routes.py`
- `tests/test_http_service.py`
- `tests/test_audit_bundle.py`
