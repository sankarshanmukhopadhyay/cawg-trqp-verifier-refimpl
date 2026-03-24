# Trust Gateway Component

## Purpose

The trust gateway introduced in v0.9.0 models remote policy mediation for CAWG–TRQP verification flows. It sits between a verifier and one or more policy services so the verifier can remain lightweight while governance logic is centrally managed.

## Why it exists

The gateway pattern is useful when:

- multiple verifiers need consistent policy mediation
- organizations want a single point for routing and policy evidence capture
- interoperability with multiple authorities or registries is required
- remote policy decisions must be auditable and exportable

## Reference implementation behavior

The gateway in this repository:

- wraps the TRQP mock service
- returns a mediation receipt alongside policy decisions
- keeps authorization and recognition semantics unchanged
- allows the verifier to switch between direct lookup and gateway-mediated lookup

## Architectural split

- Verifier: evaluates manifests, process evidence, and local execution posture
- Trust gateway: mediates policy queries and records the route taken
- Policy service: returns authorization or recognition decisions

## Result impact

When gateway mediation is enabled, the verification result includes a `gateway_mediation` object and the verification mode is marked as `gateway_mediated`.
