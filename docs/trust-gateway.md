# Trust Gateway

## Purpose

The trust gateway is an optional mediation layer between the verifier and one or more policy services.

It exists to separate verification execution, policy routing, and mediation trace production.

## Current capabilities

### Single-authority mediation

The gateway can mediate authorization and recognition lookups against a single policy service.

### Multi-authority routing

The gateway can also map `authority_id` values to distinct policy services and route labels. This lets one verifier interact with multiple policy domains while preserving a machine-readable mediation record.

## Mediation output

Each gateway-mediated lookup produces a record containing:

- `gateway_id`
- `route_label`
- `mode`
- `target_authority_id`
- `decision_type`

## Why this matters

In production systems, verifiers often should not hard-code policy endpoints directly. A mediation layer provides:

- cleaner authority separation
- more explicit routing control
- better audit evidence
- simpler migration toward federated topologies
- a reusable control point for future transport attestation work

## Interoperability role

The gateway is no longer only an internal abstraction. The repository now publishes gateway-oriented fixture packages so another implementation can test whether it preserves mediated-route behavior, target-authority selection, and verification semantics under both single-authority and multi-authority conditions.
