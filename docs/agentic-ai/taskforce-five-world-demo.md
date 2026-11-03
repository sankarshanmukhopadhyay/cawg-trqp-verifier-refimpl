---
layout: default
title: "Taskforce Five-World Demonstration"
parent: "Agentic AI Assurance"
nav_order: 7
---
# Delegated Creator Taskforce: portable experimental demonstration

**Status:** Published as part of the [v0.20.0 experimental capability baseline](../../RELEASE_NOTES_v0.20.0.md). These are **synthetic, locally executable** scenarios informed by the CAWG Delegated Creator Taskforce discussion of 23 October 2026, not an adopted CAWG specification or independent interoperability demonstration.

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

The exported report has a [Draft 2020-12 JSON Schema](../../schemas/experimental-taskforce-report.schema.json). CI validates it with `jsonschema` and rejects any attempt to label simulated results as independently assured. Independent callers can validate their copy of the JSON report without relying on undocumented Python object shapes.


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

A third party can reproduce **local synthetic decision semantics** from the
[v0.20.0 release tag](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/releases/tag/v0.20.0).
The separately tested Ed25519 statement-integrity module verifies local signatures
under supplied keys; it does **not** cryptographically authenticate the five-world
simulated delegations or establish signer identity, issuer recognition, or CAWG/C2PA
conformance. Real interoperability requires independently produced signed assets,
upstream-approved representations and trusted verification inputs. No such
cross-implementation evaluation is established by this release.

## Verification assurance contract (hardening)

The experimental kernel provides **two separate planes**:

- `authority`, `historical_authority`, `current_authority` and `coverage` represent the **simulation result** over caller-normalized data. These are **not verified assertions**, even when the simulated result reads `authorized` or `credential-backed`.
- `assured_authority=indeterminate`, `assured_coverage=unverified` and `assurance_reason=independent_evidence_verification_unavailable` are the **effective assurance outcomes** for consumers. No caller-set Boolean, opaque signature claim or unauthenticated timestamp can elevate these outcomes.

The experimental evaluator **does not accept** a caller-supplied `verified=true` as a trusted proof. A separate signature-integrity verifier exists, but it has **not** been integrated
with trusted covered-hash, identity/issuer, authority and signing-time verification
for these fixture decisions. Consequently the assured results remain
indeterminate/unverified. This is intentional fail-safe behaviour; it does not claim that missing evidence proves a negative fact.

CI includes `tests/test_taskforce_assurance_boundary.py`, including deliberate fake credential success, boundary times and tampered linked evidence. External interoperability, real credential acceptance and trusted time remain **unsupported** and are not silently waived.

### DCO privacy

Contributors using private email must set their Git author/committer to the **GitHub-confirmed** account noreply address and use a matching `Signed-off-by` trailer. The address is available in GitHub Settings → Emails. The repository's automated GitHub contribution route must be checked for matching author and trailer; a successful DCO workflow is the acceptance evidence. Do not rewrite previously published commits merely to obscure signoffs.

## Additional v0.20.0 experiments

The [Session 2 synthetic scenario catalogue](../../conformance/delegated-creator-session2-scenarios.json)
and [tests](../../tests/test_taskforce_session2_scenarios.py) add human-to-human
manager delegation, pseudonymous self-declaration/uniqueness claims, and optional
professional-licence vouching. These are **separate** experiments and do not alter
the five-world report's fixed schema or make those results independently assured.

Signer-to-organization binding and power-to-delegate claims are deliberately
non-elevating; see the [binding evaluator](../../src/cawg_trqp_refimpl/experimental_binding_assurance.py),
[adversarial tests](../../tests/test_enterprise_binding_assurance.py), and
[full traceability map](delegated-creator-trqp-traceability.md).

Run the additional scenarios with:

```bash
pytest -q tests/test_taskforce_session2_scenarios.py tests/test_enterprise_binding_assurance.py
```

## Experimental real cryptographic statement binding

The [Ed25519 statement verifier](../../src/cawg_trqp_refimpl/experimental_delegation_signature.py) validates a real signature over canonical JSON and a domain-separated experimental delegation statement, using a caller-supplied set of pinned public keys. [Tests](../../tests/test_experimental_delegation_signature.py) verify signature bytes and reject changed scope, actor, validity period, a wrong key, an unknown key and malformed signatures.

**A valid signature proves only possession of the corresponding private key and integrity of the covered statement.** It does **not** establish that the key belongs to the delegator, that CAWG accepts the issuer, that a trusted signing time exists, that revocation is current or historical, or that the statement is bound to a C2PA manifest. The fixture private key is public test material and not a deployable trust anchor. This experimental signature module is independent of the authority simulation and does not upgrade `assured_authority`.

Example:

```python
from cawg_trqp_refimpl.experimental_delegation_signature import verify_statement
result = verify_statement(envelope, {"fixture:publisher": pinned_ed25519_raw_public_key})
```

The experimental format must not be described as a CAWG delegated-creator assertion or interoperable credential. Real CAWG/C2PA conformance still requires the adopted covered-assertion layout, trusted identities, timestamp evidence and interoperability testing.
