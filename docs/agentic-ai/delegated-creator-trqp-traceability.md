---
layout: default
title: "Delegated Creator TRQP Traceability"
parent: "Agentic AI Assurance"
nav_order: 5
---
# Delegated Creator Taskforce: experimental TRQP traceability

**Status:** Informative implementation-side feasibility mapping. This is not a CAWG-adopted profile, a normative specification or a certification result.

**Discussion baseline:** CAWG Delegated Creator Taskforce, 23 and 26 October 2026. No nonpublic discussion documents are required for running the repository-local experiments. See the [machine-readable requirement mapping](../../conformance/delegated-creator-taskforce-traceability.json) and [issue #75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75).

## Two independent profile axes

- **Domain semantics:** delegated creator, self-declared subject evidence, human-to-human delegation, optional professional vouching, enterprise binding, and separate creative-role attribution. CAWG retains authority over adoption and normative profiles.
- **Operational verifier posture:** `standard`, `edge` and `high_assurance` are the repository's operational verification profiles. They are not CAWG-recognized delegated creator profiles.

## Runnable evidence

The pre-existing [five-world scenario corpus](../../conformance/delegated-creator-five-world-scenarios.json) and [demonstration](taskforce-five-world-demo.md) remain unchanged. The [Session 2 synthetic scenario corpus](../../conformance/delegated-creator-session2-scenarios.json) exercises three additional discriminating use cases:

1. A human creator authorizes a human manager for one scoped publishing action. Altered scope, false delegate identity and revocation are negative cases.
2. A pseudonymous creator asserts uniqueness. The local harness records that claim but does not verify unique personhood, identity or authority.
3. A creator presents optional professional-licence vouching. The local harness does not authenticate the issuer, bind a credential to the subject, check its revocation or confer publishing authority.

The [experimental subject-evidence evaluator](../../src/cawg_trqp_refimpl/experimental_subject_evidence.py) returns explicit unverified/indeterminate assurance outputs for externally asserted evidence. It is not a credential verifier, unique-personhood system or an authorization engine.

The [experimental signer-binding evaluator](../../src/cawg_trqp_refimpl/experimental_binding_assurance.py) consumes a signature-verification outcome but deliberately does not convert it into verified subject identity, organizational binding or authority to delegate. The existing [Ed25519 verifier](../../src/cawg_trqp_refimpl/experimental_delegation_signature.py) proves statement integrity under locally supplied pinned public keys only. Binding a key to an enterprise, evaluating signing authority, trusted signing-time evidence and historical revocation still require external authoritative evidence.

## Non-elevation invariants

| Caller-supplied evidence | Result that must **not** be inferred |
|---|---|
| Pseudonymous subject identifier | Unique human or verified legal identity |
| Claim of uniqueness | Independently assured uniqueness |
| Licence / credential claim | Recognized issuer or authority to act for a third party |
| Valid Ed25519 signature | Signer identity or enterprise authority |
| Organizational affiliation | Authority to bind an enterprise |
| Synthetic authorization at signing time | Independently assured historical authorization |

Unsupported external checks are reported as `not_checked`, `unverified` or `indeterminate` as appropriate, never implicitly as PASS.

### Verify locally

```bash
python scripts/validate_delegated_creator_traceability.py
pytest -q tests/test_taskforce_session2_scenarios.py tests/test_enterprise_binding_assurance.py
make validate
```

The new test suite uses deterministic, publicly reproducible **synthetic** cases. It cannot establish real CAWG/C2PA assertion coverage, enterprise recognition, credential issuer trust, unique human status, external TRQP interoperability, or CAWG conformance. Its negative assertions establish that these unsupported claims are not elevated.

## Upstream dependency: endorsement assertion versus delegation

The relationship between CAWG endorsement/role assertions and multi-hop scoped delegation remains an upstream decision. A repository-local experimental statement is **not** an adopted CAWG wire format. This implementation does not choose between extending an endorsement assertion and creating a separate delegation assertion.

## Completion boundary

This local increment is complete when the new scenarios, regression tests and traceability validation succeed and documented evidence matches executable behavior. It does **not** close the external interoperability gates in [#75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75). Preserve those as separately assessable dependencies.
