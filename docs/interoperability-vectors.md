# Interoperability Vectors

This repository now carries two interoperability surfaces.

The first surface is the lightweight example layer under `examples/`. These files are useful for experimentation, demos, and implementation walkthroughs.

The second surface is the canonical fixture exchange layer under `fixtures/profile-bound/`. These packages are intended for repeatable cross-implementation testing. Each package includes the request, the resolved profile, the expected result, and the pinned policy and revocation feeds needed to reproduce the decision.

## Included fixture packages

| Package | Purpose | Expected mode | Why it matters |
|---|---|---|---|
| `standard-v1` | Baseline online verification with cache-friendly semantics | `cached_online` | Establishes the default trust decision contract |
| `high-assurance-v1` | Live-only verification with fail-closed revocation posture | `online_full` | Shows the strict profile surface for stronger deployments |
| `gateway-standard-v1` | Gateway-mediated authorization and recognition | `gateway_mediated` | Demonstrates mediated transport and route evidence |
| `multi-authority-v1` | Deterministic route selection across multiple authorities | `gateway_mediated` | Shows how the gateway remains legible under federation complexity |

## What should stay stable across implementations

- resolved profile semantics
- trust outcome
- verification mode
- transport evaluation result
- revocation freshness evaluation result
- replay contract expectations
- gateway mediation fields where a fixture declares gateway participation

## What may vary safely

Implementations may differ in internal object models, logging formats, cache layouts, or deployment mechanisms. They should not differ in the externally visible decision semantics defined by the fixture package.

## Related artifacts

- `fixtures/README.md`
- `conformance/compatibility-matrix.json`
- `docs/compatibility-matrix.md`
