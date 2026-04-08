# Roadmap

## Completed in v0.7.0

1. Add process-aware verification inputs and outputs.
2. Add policy-level process requirements to authorization decisions.
3. Add parser support for process-oriented assertions in C2PA-style manifests.
4. Refresh examples, schemas, and docs for Proof of Process style integration.

## Completed in v0.8.0

1. Introduce exportable audit bundles that package verification result, policy evidence, and process appraisal together.
2. Add HTTP transport patterns for process-aware authorization and verification exchange.
3. Add benchmark fixtures for high-volume and constrained-device process-aware verification.

## Completed in v0.9.0

1. Add trust gateway component for remote policy mediation.
2. Add richer conformance and interoperability vectors.
3. Add deployment guidance for process-aware verifiers and appraisal services.

## Completed in v0.10.0

1. Stabilize audit bundle serialization profile.
2. Add assurance-oriented bundle validation and replay tooling.
3. Expand interoperability vectors toward multi-authority production patterns.

## Completed in v0.11.0

1. Add signed bundle attestation for independently verifiable export artifacts.
2. Externalize policy feeds in replay inputs so exported bundles can target pinned policy and revocation sources.
3. Add reproducibility fixtures for cross-run comparison.

## Next horizon

1. Add feed transport abstractions beyond local JSON paths.
2. Introduce revocation delta polling and feed freshness assertions.
3. Publish a cross-implementation fixture exchange profile.
