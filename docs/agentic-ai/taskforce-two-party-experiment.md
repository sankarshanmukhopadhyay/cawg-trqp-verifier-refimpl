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
