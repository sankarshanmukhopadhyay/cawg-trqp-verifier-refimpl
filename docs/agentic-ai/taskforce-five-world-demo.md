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

### Portable JSON decision report

Run `python scripts/run_taskforce_five_world_demo.py --output /tmp/taskforce-report.json` to obtain the five-world decision report with per-scenario expected versus actual outcomes and explicit `independent_crypto_verification=false` and `independent_interoperability=false` flags. The report is deterministic and its CLI contract is regression-tested; it is not a cryptographically certified output. The `assured_authority` and `assured_coverage` fields are the applicable assurance-boundary outputs, never the simulated authorization labels.

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

## Verification assurance contract (hardening)

The experimental kernel provides **two separate planes**:

- `authority`, `historical_authority`, `current_authority` and `coverage` represent the **simulation result** over caller-normalized data. These are **not verified assertions**, even when the simulated result reads `authorized` or `credential-backed`.
- `assured_authority=indeterminate`, `assured_coverage=unverified` and `assurance_reason=independent_evidence_verification_unavailable` are the **effective assurance outcomes** for consumers. No caller-set Boolean, opaque signature claim or unauthenticated timestamp can elevate these outcomes.

The experimental evaluator **does not accept** a caller-supplied `verified=true` as a trusted proof. Until an actual cryptographic signature, covered-hash, issuer authorization, trust anchor, and signing-time verifier is implemented and integrated, the assured results must remain indeterminate/unverified. This is intentional fail-safe behaviour; it does not claim that missing evidence proves a negative fact.

CI includes `tests/test_taskforce_assurance_boundary.py`, including deliberate fake credential success, boundary times and tampered linked evidence. External interoperability, real credential acceptance and trusted time remain **unsupported** and are not silently waived.

### DCO privacy

Contributors using private email must set their Git author/committer to the **GitHub-confirmed** account noreply address and use a matching `Signed-off-by` trailer. The address is available in GitHub Settings → Emails. The repository's automated GitHub contribution route must be checked for matching author and trailer; a successful DCO workflow is the acceptance evidence. Do not rewrite previously published commits merely to obscure signoffs.

## Experimental real cryptographic statement binding

The [Ed25519 statement verifier](../../src/cawg_trqp_refimpl/experimental_delegation_signature.py) validates a real signature over canonical JSON and a domain-separated experimental delegation statement, using a caller-supplied set of pinned public keys. [Tests](../../tests/test_experimental_delegation_signature.py) verify signature bytes and reject changed scope, actor, validity period, a wrong key, an unknown key and malformed signatures.

**A valid signature proves only possession of the corresponding private key and integrity of the covered statement.** It does **not** establish that the key belongs to the delegator, that CAWG accepts the issuer, that a trusted signing time exists, that revocation is current or historical, or that the statement is bound to a C2PA manifest. The fixture private key is public test material and not a deployable trust anchor. This experimental signature module is independent of the authority simulation and does not upgrade `assured_authority`.

Example:

```python
from cawg_trqp_refimpl.experimental_delegation_signature import verify_statement
result = verify_statement(envelope, {"fixture:publisher": pinned_ed25519_raw_public_key})
```

The experimental format must not be described as a CAWG delegated-creator assertion or interoperable credential. Real CAWG/C2PA conformance still requires the adopted covered-assertion layout, trusted identities, timestamp evidence and interoperability testing.
