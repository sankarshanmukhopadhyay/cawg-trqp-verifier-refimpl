# Integration Guide

The repository now supports four operational integration patterns:

1. direct verifier invocation against a live TRQP-style policy service
2. gateway-mediated verification where route metadata becomes part of the evidence surface
3. offline verification against a signed snapshot for edge-style environments
4. fixture-driven replay for interoperability and assurance work

## Direct flow

Manifest -> verifier -> policy service -> process appraisal -> verification result

This is the simplest integration path. It is appropriate when the verifier can contact policy and revocation feeds directly and when the deployment tolerates cache-first behavior.

## Gateway-mediated flow

Manifest -> verifier -> trust gateway -> policy service -> verification result + gateway mediation trace

This flow is appropriate when policy access is routed through a mediation layer, when multiple authorities must be selected deterministically, or when the deployment wants a stable route evidence surface.

## Offline or edge flow

Manifest -> verifier -> signed snapshot -> verification result

This flow is for environments where live connectivity is not expected. It preserves a strong audit story by requiring signed snapshot material and trust anchors rather than pretending the system is live when it is not.

## Fixture exchange flow

Fixture package -> implementation under test -> verification result -> compatibility comparison

This is the adoption-focused path added in the current increment. It allows the repository to function as a conformance handoff artifact rather than only as source code.

## Recommended implementation sequence

Start with direct flow, add gateway-mediated support if your environment centralizes policy access, then consume the canonical fixture packages to prove that your implementation preserves the expected decision semantics.
