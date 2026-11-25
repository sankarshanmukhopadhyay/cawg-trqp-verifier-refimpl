---
layout: default
title: "Taskforce Two-Party Integrity Experiment"
parent: "Agentic AI Assurance"
nav_order: 8
---
# Two-party delegation integrity experiment

Sessions 5 (20 November 2026) and 6 (23 November 2026) motivate this local
experiment. Engineering tracker: [#75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75).
Living progress: [#107](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/107).

The proposed path D is not a ratified CAWG credential format. This module
extends the existing Ed25519 statement experiment without modifying stable
APIs. It checks two role-specific signatures covering identical delegation
terms, key identifiers and a supplied context digest. Distinct keys are
required. The digest is not independently verified C2PA manifest coverage.

Run:

```bash
pytest -q tests/test_experimental_two_party_delegation.py
make validate
```

A verified integrity result establishes signature validity under supplied
keys only. Recognized subject/key binding, authority to delegate, independent
consent, trusted time, status and actual asset coverage remain unestablished.
The delegate signature is not inferred to be consent, and a guardian or
witness cannot be inferred from signature count. No external references are
fetched; output does not expose parties or delegation terms.

Fixture keys are public test material, not deployable trust roots. External
registry, consent and signed-asset evidence remain required for stronger
claims. Do not describe this experiment as CAWG interoperability.

## Integrated operation assessment and Wave 1

The [operation assessment](../../src/cawg_trqp_refimpl/experimental_taskforce_assessment.py)
combines two-party integrity, signed-term matching, claimed consent scope and
subject evidence in a single local consumer path. It compares the request's
principal, actor, action, resource, purpose, time and context with the signed
statement. It does not grant authority. The two consent and delegation
lifecycles remain separately visible. Consent may concern a subject other than
the delegate. A missing consent subject does not mean consent is unnecessary.

The [Wave 1 coverage catalog](../../conformance/delegated-creator-wave1-coverage.json)
reuses prior scenario baselines and adds a bounded influencer sponsorship
mapping. It covers the six use cases identified on 23 November 2026.
It records the mandatory question identifiers Q5, Q6, Q9 and Q10 without
asserting that local experiments settle the questions or constitute adopted
specification issues. The exact CAWG assertions and the full question/controls
matrix require upstream review.

```bash
pytest -q tests/test_experimental_two_party_delegation.py tests/test_taskforce_wave1_assessment.py
make validate
```

Public output is allowlisted. Verification does not dereference private
consent references or resolve an opaque identifier. Claimed registry status
does not authenticate a registry, its governance or the asserted key binding.
A status-list or other network retrieval mechanism would require explicit
authorization, bounded retrieval, verified source authority and a privacy
review; it is not introduced here. Current and historical scope labels concern
signed terms or caller-supplied consent claims, not independently established
revocation or historical authority. A two-party signature does not establish
guardian authority, witness authority, legal consent, public disclosure
compliance or creative credit.

The catalog is a local, executable coverage reconciliation, not six authentic
signed C2PA assets or complete Taskforce use-case submissions. Authentic
assets, trusted time, recognized registry/consent status, industry schema
semantics and independent reproduction remain external gates in #75.

## Offline authenticated source evidence (local experimental body)

The [source evidence adapter](../../src/cawg_trqp_refimpl/experimental_source_evidence.py)
reuses the existing signed feed descriptor validation and adds strict source
key/authority/scope binding, exact body matching, explicit observation time,
bounded input bytes, duplicate-JSON rejection and fail-closed freshness checks.
It does not define a CAWG credential, TRQP response or status-list format.

Pass already available descriptor/body byte pairs through the operation
assessment's optional `source_packages` argument. The relying party separately
configures `source_policies` using `PinnedEvidenceSource` (expected kind,
authority identifier, key identifier, Ed25519 public PEM and maximum age).
Supply `source_observed_at` from the relying party's clock; it must match the
operation's evaluation instant. Neither the evidence nor an asset can select
its own trust policy, initiate a fetch or upgrade the time of use.

The experimental body is a JSON object with exactly `profile`
(`experimental-taskforce-source-claim/0.1`), `kind`, `claim` and `state`.
Each descriptor binds the exact body bytes, uses the existing descriptor
version 1.0.0, and contains the scope `experimental-taskforce:<kind>`.

| Package key | Kind | Exact claim fields | Allowed source states |
|---|---|---|---|
| delegator_binding, delegate_binding | subject-key-binding | subject_ref, key_sha256 (raw Ed25519 public key) | active, revoked, suspended, unknown |
| authority_to_delegate | authority-to-delegate | statement_sha256, delegator_key_sha256, delegate_key_sha256 | active, denied, revoked, unknown |
| delegation_status | delegation-status | same exact signed-terms and key digests | active, revoked, suspended, unknown |
| consent_record | consent-record | subject_ref, record_sha256 (canonical normalized consent record) | attested, disputed, unknown |

The statement digest is SHA-256 of the existing role-bound delegator signing
bytes; the context digest is included. The delegation-status package uses a
revocation feed descriptor; others use a policy feed descriptor. A consent
receipt authenticates a source's attestation to a normalized record, not the
bytes behind its private reference or legal permission. A current observation
does not prove an earlier signing-time state. The operation output exposes
only status/state/reason, never raw evidence, keys, subjects or URLs.

`authenticated_source_claim` means the explicitly configured key signed the
matching body and freshness conditions passed. It does **not** establish
independent governance of that key, a recognized CAWG/TRQP authority, trusted
historical time, valid consent, or actual C2PA assertion coverage. Even a
locally authenticated active claim does not elevate `assured_authority` or
`assured_consent`; a revoked, denied or disputed source state remains visible.
Independent recognition of the source policy and genuine external evidence are
still required. No source key independence or legal identity is inferred
from distinct identifiers.

```bash
pytest -q tests/test_experimental_taskforce_source_evidence.py
make validate
```

The tests use a separate deterministic fixture source key to authenticate
local evidence, exercise substitution, unknown source, wrong scope, stale
and future evidence, revoked status and consent-record replay. These are
local integration tests, not evidence of external trust governance.
