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
