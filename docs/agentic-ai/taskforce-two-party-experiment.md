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

## Public report contract

The [operation report schema](../../schemas/experimental-taskforce-operation.schema.json)
defines a closed output vocabulary. Unsupported assurance, identity, trusted
time and asset-binding results cannot be advertised as verified. The schema
also rejects a positive signed-term applicability result after failed or
indeterminate signature integrity, unauthenticated source states advertised as
active, and undeclared output fields. Schema validation checks report shape and
invariants; it is not an alternative to executing the verifier.

```bash
pytest -q tests/test_taskforce_operation_report_schema.py
make validate
```

## Reproduce Wave 1 and question reconciliation

```bash
python scripts/run_taskforce_wave1_demo.py --output /tmp/taskforce-wave1.json
pytest -q tests/test_taskforce_wave1_demo_cli.py tests/test_taskforce_multi_recipient_isolation.py tests/test_taskforce_session5_6_traceability.py
```

The public fixture keys are intentionally reproducible and never production
trust roots. The CLI runs the actual assessment, validates the report schema,
checks a wrong-actor counterexample for every case, and exits nonzero if the
expected results differ. It makes no independent interoperability claim.
The [Q1–Q23 crosswalk](../../conformance/delegated-creator-session5-6-questions.json)
records the local contribution and unresolved decisions for every question.
The Wave 1 catalog records candidate assertions and provisional answers to
Q5, Q6, Q9 and Q10. These are not approved Taskforce use-case submissions.

For Q23, independent two-party records per recipient are sufficient to
demonstrate isolation of acceptance, scope, renewal and consent. A missing
countersignature cannot verify; we do not claim to implement a pending
workflow, a shared multi-recipient credential, or collective acceptance.
The source and format of authoritative per-recipient lifecycle evidence
remain external decisions.

### Informative policy and disclosure boundaries

The 23 November discussion grouped requirements into public disclosure,
subject consent and safeguards for minors/intimate images. The sponsorship
worked example names the FTC Endorsement Guides and, where a synthetic
performer is involved, New York disclosure requirements. The verifier can
help establish evidence for a claim, not determine legal applicability,
rights, liability, insurance, certificate funding, removal obligations or
guardianship. A minor's guardian signature requires separate proof of the
relationship and authority under applicable policy. Do not infer that consent
is unnecessary merely because no consent record was supplied. Public
sponsorship verification is not equivalent to the obligation to disclose
sponsorship; absence of proof is not proof of absence of a paid relationship.

The privacy risk is not confined to private agreement retrieval: a
per-viewer status query can also reveal activity. Offline evidence avoids
these calls in this experiment. A future status-list design must separately
consider distribution, caching, freshness, revocation latency, correlation
and access authorization. No issuer call or private detail fetch is needed
to reproduce these local tests.

### Case-specific question answers and ambiguity controls

The Wave 1 catalog contains separate provisional story cards and responses
to Q5, Q6, Q9 and Q10 for each case. It records candidate assertions,
applicable verifier tests, extensions, and policy-review questions. These
are implementation-side proposals, not Taskforce-assigned use-case ownership
or normative submissions. The Taskforce's use-case method refers to issue
#286; no new upstream issues are created or assigned here.

The [candidate controls matrix](../../conformance/delegated-creator-session5-6-controls.json)
maps ten consequential ambiguity/failure conditions to the living inventory,
local tests and upstream questions. It is an implementation contribution to
the controls-matrix discussion scheduled for 4 December 2026, not an adopted
matrix or viewer UI. In particular, the verifier must not show a verified
sponsorship from signature validity alone, and absence of a verified label
must not be interpreted as an absence of sponsorship or disclosure duty.

The twelve legal/policy entries discussed on 23 November were grouped into
disclosure (EU AI Act Article 50, California AI Transparency Act, New York
synthetic performer rules, FTC Endorsement Guides), consent (California
AB 2602/AB 1836, Tennessee ELVIS Act, Denmark copyright proposal, US NO FAKES
Act proposal), and minors/intimate images (GDPR Article 8, Italy Law 132/2025,
amended COPPA rule, TAKE IT DOWN Act). This is a record of the discussion
topics, not independent verification of legal status, scope, or applicability.
No verifier control substitutes for a legal assessment of each use case.
