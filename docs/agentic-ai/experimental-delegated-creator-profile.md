---
layout: default
title: "Experimental Delegated Creator Profile"
parent: "Agentic AI Assurance"
nav_order: 6
---
# Experimental Delegated Creator application profile 0.1

**Status:** repository-local engineering experiment, **not** an adopted CAWG/TRQP specification, conformance suite, credential verifier or C2PA manifest validator. Tracks [issue #73](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/73) and follows the [taskforce mapping](delegated-creator-trqp-traceability.md).

## Proposition and architecture

Investigate DC-01 through DC-06 using a deterministic decision kernel driven by *already extracted* creator/delegation evidence. The experiment deliberately does not modify production verifier APIs, the three existing operational assurance profiles, or released conformance contracts. The [machine-readable experimental profile](../../conformance/experimental-delegated-creator-profile.json) is separate from those operational profiles.

**Input trust boundary:** The caller supplies a normalized case with signer time, evaluation time, root principal, action/resource/purpose, delegation chain, external linked evidence payloads, and generator policy. This layer has no C2PA parser, signing key, credential issuer integration or TRQP network resolver. An input flag such as `credential_verified` merely *simulates* an upstream credential verification assertion and MUST NOT be used as independent proof of credential authenticity.

## Selected use-case experiments (DC-01)

1. **Direct creative publishing:** creator delegates a studio to publish one asset for editorial purposes; signed within validity interval.
2. **Agentic publishing:** a studio subdelegates a narrower `publish` right to an agent within inherited scope and duration; scope expansion fails.
3. **Unverified creator claim:** a generator sees no supporting delegation; it rejects by default; a generator configured to accept still cannot turn indeterminate authority into authorization.

These are **illustrative scenarios**, not the taskforce's approved five-world use-case set.

## Opinionated constraints

- **DC-02:** delegation evidence lives outside the content payload in an HTTPS reference and content SHA256; the experiment verifies supplied fixture bytes, *not* a remote agreement or manifest binding. Both signing-time and evaluation-time status are separately evaluated.
- **DC-03:** coverage `unverified`, `delegator-covered`, `credential-backed` is an **evidence class**, not an authorization outcome. Credential-backed remains hypothetical until a trusted issuer verifier is integrated. Missing evidence stays indeterminate.
- **DC-04:** chain rooted at an explicitly named principal; at most three links, at most 30 days per link; no cycles; each child action/resource/purpose set and expiry must be a subset of its parent's scope/end. Revocation at signing time or evaluation time produces distinct reason codes. These numeric limits are **experimental defaults**, not CAWG decisions.
- **DC-05:** a local generator has a decision to reject indeterminate evidence, with recorded reason and authority result. `accepted` means generator processing was allowed by this fixture policy, **not** that a third cryptographic signature was applied, or that the actor is authorized.
- **DC-06:** the profile version and assumptions are machine-readable and the decision kernel is exercised by adversarial tests. No upstream conformance is claimed.

## Usage

```bash
pytest -q tests/test_experimental_delegated_creator.py
make validate
```

Programmatic integration:

```python
from cawg_trqp_refimpl.experimental_delegated_creator import evaluate
result = evaluate(normalized_case)
```

Results include `case_id`, `profile`, `coverage`, `authority`, `generator`, stable `reason`, evaluation time and a digest of the evaluated chain when available. Failure semantics: malformed input raises `InvalidCase`, insufficient or tampered evidence gives `indeterminate`, and policy violations give `denied`. This experiment has no side effects.

## Falsification and remaining boundaries

The tests probe out-of-scope action, temporal boundaries, revocation at signing and evaluation, evidence tampering, chain break, cycle, depth overflow, duration overflow, re-delegation prohibition, scope escalation, unverified generator processing, and deterministic replay.

This is **not** a full C2PA implementation. It deliberately cannot establish that the supplied root principal was in fact the original consenting party; that a linked agreement is legally sufficient; that a timestamp is cryptographically trusted; that `credential_verified` is true; or that generator acceptance results in a C2PA cryptographic signature. Actual remote evidence retrieval, authentic credential validation, trust anchor processing and cross-implementation interoperability are excluded.

## Upstream decisions that would change this experiment

CAWG must still decide the definitions of coverage, signing-time manifest binding and evidence references, chain semantics and limits, whether the claim generator is a distinct cryptographic signer, and the normative subset of TRQP. Revisions should be versioned and backed by compatibility/conformance fixtures. The upstream survey DC-07 is external and is not implemented here.
