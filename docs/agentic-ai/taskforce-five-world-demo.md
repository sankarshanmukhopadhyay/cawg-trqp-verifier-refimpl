---
layout: default
title: "Taskforce Five-World Demonstration"
parent: "Agentic AI Assurance"
nav_order: 7
---
# Delegated Creator Taskforce: portable experimental demonstration

**Provenance:** CAWG Delegated Creator Taskforce kick-off slides and minutes, 23 October 2026. These are proposed requirements, **not an adopted specification**.

## Run

```bash
python -m pip install -r requirements-lock.txt
python -m pip install -e .
pytest -q tests/test_experimental_delegated_creator.py tests/test_taskforce_five_worlds.py tests/test_experimental_assertion_order.py
make validate
```

[Input scenario catalog](../../conformance/delegated-creator-five-world-scenarios.json), [eight-test assessment](../../conformance/delegated-creator-taskforce-eight-tests.json), [executable model](../../src/cawg_trqp_refimpl/experimental_delegated_creator.py), [fixture test runner](../../tests/test_taskforce_five_worlds.py).

The five portable scenario descriptions represent agency handover, AI voice tool, VFX subdelegation, freelance reporter, and photography assistant. Each has an expected historical authorization decision, current status, and adversarial mutation. The test runner maps these into synthetic normalized inputs, verifies expected decisions, and demonstrates deterministic replay.

## Assurance boundaries and semantics

- **Historical authority is not current authority.** Later expiry or revocation does not retroactively alter a valid signing-time delegation; new signatures after revocation fail. Revocation metadata and signing times in these fixtures are **caller supplied**, not signed or independently verified.
- **Evidence provenance is explicit:** generator decisions are simulated; credential verification is caller-supplied; delegator signature is not cryptographically checked; linked content is checked against a local digest only. `credential-backed` and `delegator-covered` are *simulated classification labels* and must not appear as externally verified claims.
- **Authority is not authorship.** The news and photography stories deliberately carry creative-credit metadata independently of the authority evaluator. That metadata does not become proof of authorship.
- **Contracts are not distributed in decisions.** Fixture inputs have local content for digest checks; exported output is designed to contain references and digests, not private agreement terms.
- **No network requests.** Real C2PA parsing, trusted timestamp evidence, identity/issuer anchors, signatures, credential revocation and trust-list or TRQP interoperability are not implemented by this experimental module.
- **The coverage ladder is provisional.** Actual levels 2 and 3 require authority-signature and accepted-issuer evidence absent from this prototype.

## Eight-test interpretation

The [machine-readable matrix](../../conformance/delegated-creator-taskforce-eight-tests.json) intentionally includes `demonstrated`, `simulated`, `partial` and `unsupported` dispositions. The Taskforce's signature ordering (delegation, delegator signature, delegate signature, manifest seal) has a local [acyclic, ordered reference-structure check](../../src/cawg_trqp_refimpl/experimental_assertion_order.py) with [negative vectors](../../tests/test_experimental_assertion_order.py). It does **not** validate cryptographic signatures or covered hashes, so claiming the complete signing-order requirement as passing would be misleading.

## External consumption gate

A third party can reproduce **local synthetic decision semantics**, not independent cryptographic verification, credential recognition or CAWG/C2PA conformance. Real interoperability requires another implementation and authoritative upstream formats and trust anchors. No such evaluation has been conducted. No new release or normative version is implied.
