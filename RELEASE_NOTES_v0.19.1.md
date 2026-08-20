# CAWG-TRQP Verifier Reference Implementation v0.19.1

## TRQP Portfolio Alignment and Assurance Closure

v0.19.1 establishes an explicit, machine-verifiable relationship between this CAWG/C2PA-oriented reference implementation and the synchronized TRQP assurance stack. It also snapshots the post-v0.19.0 assurance work already present on `main`, including RAHP finding closure, agentic-AI assurance, expanded walkthroughs, and refreshed presentation evidence.

This release does not give this repository normative authority over CAWG, C2PA, or TRQP. Repository authority remains limited to implementation behavior, local schemas, profiles, fixtures, and evidence.

## Portfolio integration

The release adds `portfolio/integration-contract.json` and pins:

- Trust Systems Meta-Model v0.24.0 as semantic authority;
- Trust Infrastructure Schemas v0.14.1 as schema and portfolio authority;
- TRQP-TSPP v0.15.0 as the TRQP protocol/profile baseline implemented against;
- TRQP Conformance Suite v1.7.0 as the conformance evidence consumer;
- TRQP Assurance Hub v1.10.0 as the assurance aggregation consumer.

The contract declares explicit invalidation triggers for incompatible semantic/schema authorities, incompatible normative sources, missing required evidence, and release-identity mismatch. CI validates those conditions through `scripts/validate_portfolio_contract.py`.

## Release and evidence integrity

- Updated package and citation identity to v0.19.1.
- Aligned `conformance/compatibility-matrix.json` and `conformance/assurance-suite-manifest.json` with the current release instead of their stale v0.16.0 identity.
- Added TRQP authority/component pins to machine-readable conformance evidence.
- Made release checksum generation derive the target release from `pyproject.toml` instead of a hard-coded version.
- Added the portfolio integration contract to release checksum evidence.
- Preserved v0.19.0 checksum evidence as historical release evidence rather than rewriting it.

## Assurance work included since v0.19.0

The release also captures work already present on `main` after v0.19.0:

- profile-defined degraded-result disposition for unresolved mandatory semantic predicates;
- explicit snapshot authority-state age and stale deny/defer evidence;
- evidence sensitivity, retention, redaction, and disclosure-audience metadata;
- visible relying-party precedence and source classification in conflict evidence;
- machine-validated RAHP-to-control/test traceability;
- a cross-cutting Agentic AI Assurance model covering delegated producer, submitter, verifier, orchestrator, proxy, and decision roles;
- expanded sector and cross-sector walkthrough coverage with authority, delegation, revocation, replay, correction, and redress expectations;
- refreshed non-normative presentation evidence and drift validation.

## Compatibility

The v0.19.1 portfolio-alignment changes do not alter CAWG/C2PA verification semantics or the TRQP service interface. Existing profiles, request/response structures, receipts, audit bundles, and replay behavior remain compatible with the v0.19.0 semantic-assurance baseline.

The new integration contract is an assurance boundary: downstream consumers can now determine whether this implementation is being interpreted against the intended TRQP semantic, schema, conformance, and assurance versions.

## Validation

The release gate is:

```bash
make validate
python scripts/validate_portfolio_contract.py
python scripts/export_conformance_pack.py --check
python scripts/generate_release_checksums.py --check
```

GitHub Actions additionally runs the supported Python-version matrix and release evidence checks.
