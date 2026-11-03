# CAWG–TRQP Verifier Reference Implementation v0.20.0

**Experimental Delegated Creator and Assurance Evidence**  
**Release date:** 3 November 2026  
**Classification:** Experimental capability release; the stable verifier interfaces and operational profiles remain the previously established reference implementation surface.

## Summary

This release establishes a versioned and reproducible experimental baseline for studying creator delegation and the evidence needed to assess whether a person, organization, or automated system may act for another party in a content creation or publication workflow.

The release collects the experimental work merged after v0.19.2, including bounded delegation-chain evaluation, synthetic cross-sector cases, actual cryptographic statement-integrity checks using local keys, separate evidence states for issuer/vouching and organizational authority, an optional guarded C2PA validation adapter, and portable test reports. It also improves repository validation and publication maintenance.

**This is not a CAWG-endorsed delegated-creator implementation, production authorization service, certification, or independent interoperability demonstration.** The experimental modules operate on synthetic or caller-normalized evidence and cannot establish trusted identity, issuer recognition, enterprise authority, trusted signing time, or validity of signed CAWG delegation assertions.

## What users and integrators can do

### 1. Reproduce five representative delegated-creation cases

The five-world synthetic corpus exercises:

- brand-to-agency content handover;
- scoped AI voice-tool use;
- studio/vendor multi-hop delegation;
- publisher/freelance reporter relationships;
- photographer/assistant activity.

A deterministic command exports a JSON decision report with expected-versus-observed outcomes. A JSON Schema constrains the report and prevents a simulated result from being represented as independently assured authorization. Negative tests include scope violations, expiry, revocation, chain-depth boundaries, and evidence tampering.

The local evaluator separates authority **at the caller-supplied signing time** from a **caller-supplied current evaluation time**. Neither time is independently attested. A previously valid hypothetical delegation is not automatically rewritten when it later expires or is revoked; this is a simulation of temporal logic, not proof of historical legal authority.

### 2. Examine additional creator and vouching relationships

Three additional synthetic scenario families cover:

- human-to-human manager delegation;
- pseudonymous/self-declared creators claiming uniqueness without identity disclosure;
- optional professional-licence vouching.

Experimental subject-evidence classification records the declared evidence while retaining unverified or indeterminate assurance where no independent verification exists. A claimed licence, pseudonymous identifier, or uniqueness statement does **not** authorize action for a third party.

### 3. Test the difference between signature integrity and permission

The experimental Ed25519 statement verifier cryptographically checks a domain-separated canonical delegation statement against caller-supplied pinned public keys. Negative cases include modified scope, actors and time bounds, invalid signatures, unknown keys and malformed input.

That check establishes **statement integrity under the supplied key**, not identity ownership, trusted certification, enterprise affiliation, authority to bind, or C2PA manifest coverage. Separate signer-binding tests demonstrate that even a valid signature and claimed organizational relationship cannot independently elevate the assured authorization outcome.

### 4. Evaluate a constrained external C2PA validator boundary

The optional `c2patool` subprocess boundary provides bounded invocation and machine-readable receipts, including absent-tool, invalid-report and timeout/error handling. Mock-driven integration tests exercise failure behavior and preserve explicit non-elevation of delegated authority.

**No independent signed-asset run, accepted external trust bundle, live TRQP registry query, or cross-implementation Delegated Creator validation has been established by this release.** The adapter is a feasibility interface, not an interoperability certification.

### 5. Reproduce evidence without distributing private agreements

The experimental decision reports avoid embedding private contract or consent contents; local synthetic input may include sample linked material for deterministic digest checks. The tests distinguish structural assertion ordering from cryptographic signature or C2PA covered-hash verification. Local signing and assertion-order experiments are separate from the stable verifier's existing enforcement posture.

## Validation and assurance evidence

The repository-wide `make validate` gate includes machine-readable requirements traceability, synthetic scenarios, positive/negative and regression tests, schema validation, deterministic report generation, external-adapter mock tests, and the repository's existing policy, transport, audit, replay and documentation checks.

The release workflow runs this gate again at the release commit, builds a Python source distribution and wheel, and attaches a SHA-256 manifest for selected conformance, integration and replay artifacts. The checksum manifest identifies release-pinned inputs, not a third-party audit or certification.

The experimental Taskforce eight-test matrix preserves `demonstrated`, `simulated`, `partial`, and `unsupported` distinctions. Local cryptographic integrity does not upgrade the unsupported CAWG manifest-coverage or credential-issuer trust tests.

### Reproduce locally

```bash
python -m pip install -r requirements-lock.txt
python -m pip install -e .
python scripts/run_taskforce_five_world_demo.py --output /tmp/taskforce-report.json
pytest -q tests/test_taskforce_session2_scenarios.py tests/test_enterprise_binding_assurance.py
make validate
```

The input fixture catalogs are `conformance/delegated-creator-five-world-scenarios.json` and `conformance/delegated-creator-session2-scenarios.json`. The portable output contract is `schemas/experimental-taskforce-report.schema.json`. Run `python scripts/generate_release_checksums.py --check` only against a generated checksum manifest; the published manifest is attached to the GitHub release rather than committed to the source tree.

## Compatibility, versioning and adoption

- **No intentional breaking change** to stable verification APIs, operational profiles (`standard`, `edge`, `high_assurance`), or existing five-world result semantics has been introduced in this release tranche.
- The new Delegated Creator, subject-evidence, and signer-binding surfaces are explicitly **experimental** and repository-local. Consumers must not treat their names, coverage classes, or wire representation as CAWG-defined interoperability contracts.
- The experimental profile's maximum three-hop chain and 30-day per-link validity are test defaults, not requirements prescribed by CAWG.
- Existing TRQP semantic/schema and conformance-component version pins are retained; a repository release does not imply upstream version adoption or approval.
- Integrators should retain their own relying-party authorization policy and independently supply trusted identity, issuer, revocation and timing evidence where decisions require it.

## Known limitations and outstanding work

- No accepted CAWG Delegated Creator assertion representation, C2PA covered-hash/signature binding, or upstream endorsement/delegation mapping has been validated.
- No independently established creator uniqueness, subject-to-key/enterprise identity linkage, organizational authority-to-bind, or accepted professional issuer status.
- No trusted signing-time evidence, live historical revocation evidence, real TRQP v2.0 trust-endpoint recognition response, or verified reusable credential trust chain.
- No demonstrated independent C2PA/TRQP cross-implementation agreement using externally produced, licensed signed assets and trust anchors.
- The synthetic results are not proof of legal rights, attribution, consent sufficiency, copyright ownership or authorship.
- Benchmarks, documentation scenarios and local tests do not assert production deployment readiness or throughput guarantees.

These limitations remain tracked in [issue #75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75); it is intentionally **not closed** by this experimental release.

## Other changes since v0.19.2

- Publication-state documentation and release-evidence consistency checks were strengthened.
- Developer contribution and governance controls gained a DCO workflow, branch housekeeping, and managed dependency updates.
- A public-documentation link audit was added with artifact evidence capture; its artifact uploader was upgraded.
- The release workflow now reads **version-matched release notes** rather than republishing a hardcoded earlier release description. It checks the build and checksum artifacts and explicitly publishes the GitHub release as **latest**.

## Provenance and release scope

This release is maintained by the repository owner as a **reference implementation and research/feasibility artifact**. CAWG, C2PA, TRQP and related external authorities retain their own specification, assurance and conformance governance. The 23 and 26 October 2026 Taskforce discussions informed local scenario exploration; no nonpublic meeting documentation is bundled or required for reproduction.

**Changes:** [v0.19.2...v0.20.0](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/compare/v0.19.2...v0.20.0)  
**Documentation:** [Taskforce five-world demonstration](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/blob/v0.20.0/docs/agentic-ai/taskforce-five-world-demo.md) · [Assurance traceability](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/blob/v0.20.0/docs/agentic-ai/delegated-creator-trqp-traceability.md) · [External C2PA boundary](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/blob/v0.20.0/docs/external-c2pa-validation-boundary.md)

**Release assets:** source distribution, Python wheel, and `checksums-v0.20.0.json` plus automatically generated GitHub source archives.
