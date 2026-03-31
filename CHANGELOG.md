# Changelog

## v0.10.0

- stabilize the audit bundle serialization profile with deterministic digest and bundle identifier fields
- add audit bundle schema validation and replay tooling
- add replay inputs to exported bundles so assurance workflows can re-execute trust decisions
- add multi-authority gateway routing and production-style interoperability vectors
- harden the HTTP wrapper to separate verification request fields from transport control fields
- expand test coverage for deterministic export, replay, and gateway routing

## v0.9.0

- add exportable audit bundle support that packages verification result, policy evidence, process appraisal, and gateway mediation
- add trust gateway component for remote policy mediation
- expand HTTP transport patterns with verify and audit bundle endpoints
- add benchmark fixtures for high-volume and constrained-device verification
- add richer interoperability vectors and deployment guidance
- add non-technical overview for enterprise IT and business leaders

## v0.7.0

- add process-aware verification inputs and outputs
- add policy-level process requirements to authorization decisions
- add parser support for process-oriented assertions in C2PA-style manifests
- refresh examples, schemas, and docs for Proof of Process style integration
