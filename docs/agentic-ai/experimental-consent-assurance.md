---
layout: default
title: "Experimental Consent Assurance"
parent: "Agentic AI Assurance"
nav_order: 7
description: "Independent, experimental consent evidence classification and its limits."
---
# Experimental consent evidence assessment

**Status:** informative repository-local experimental evaluator, **not** CAWG ratification, verified performer consent, rights adjudication, legal advice, consent registry, or production authorization. The work addresses public discussion themes concerning creator delegation, likeness/voice consent, intended-use scope and withdrawal. No unpublished Taskforce documents are reproduced or required.

## Evidence dimensions

A content signature shows statement integrity under a key. Creator identity or organizational affiliation does not establish permission to act. Scoped delegation does not establish consent from a person appearing or heard in content. A consent claim in turn does not authorize a studio, platform or AI tool to publish on behalf of another party. The evaluator deliberately keeps these questions independent.

`assess_consent(case)` accepts caller-normalized consent assertions with a subject reference, intended action/resource/purpose, time of use, evaluation time and a bounded list of evidence references. A consent record specifies its claimed scope, validity, effective withdrawal time, observed withdrawal time and an HTTPS reference with a supplied digest. The evaluator **does not retrieve or validate the referenced bytes, authenticate consent signatures, establish subject-to-key binding, or resolve trusted issuer/registry state**. Every apparent match is therefore **claimed**, not independently verified. Matching SHA-256-looking text is not proof of an agreement's content or authenticity.

The output reports `consent_evidence_status`, `consent_scope_status`, `consent_at_use_time`, `consent_current_state`, `assured_consent`, `consent_time_provenance` and a stable `reason`. `assured_consent` remains `indeterminate` for all locally supplied fixtures. Missing records are not interpreted as evidence that consent was never given. Contradictory records cannot silently authorize a use.

## Temporal treatment and privacy

An asserted withdrawal effective after an earlier use does not retroactively erase that earlier claim. Whether the use remains legally permissible, or whether previously published material must be removed, is outside the evaluator. A retrospective withdrawal not observed as of an evaluation time cannot become a certain current-state finding. All use and withdrawal timestamps are **caller supplied and untrusted**. Historical authenticity and continuing permission are separate relying-party decisions.

The public assessment does not emit the subject identifier, raw agreements, evidence links or consent terms. Registry access policies, role-based disclosure, consent authority, retention and evidence authenticity must be supplied by an external governed system. This experiment must not be used to bypass consent obligations.

## Reproduce

```bash
python scripts/run_taskforce_consent_demo.py
pytest -q tests/test_experimental_consent_assurance.py tests/test_experimental_consent_temporal.py tests/test_taskforce_consent_scenarios.py
make validate
```

Two synthetic scenarios examine brand/agency/performer and studio/AI-voice/performer relationships. Output is deterministic and machine-readable; `independent_consent_verification=false` and `independent_interoperability=false`. See [the scenarios](../../conformance/delegated-creator-consent-scenarios.json) and [traceability mapping](../../conformance/delegated-creator-consent-traceability.json).

## Upstream and external dependencies

CAWG decides delegation/endorsement interoperability, agreed vocabulary and conformance. Real C2PA assertion coverage, independently recognized role and issuer evidence, historical signing time, registry trust, consent authenticity and independent implementation agreement remain external. [Issue #75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75) tracks the pre-existing external gate. The repository must not present synthetic scenario success as completion of that gate.
