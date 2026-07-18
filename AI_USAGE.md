---
layout: default
title: "AI Usage"
description: "Repository policy for transparent and accountable use of AI-assisted tooling."
nav_order: 11
---
# AI Usage Policy

## Purpose

This repository permits AI-assisted tooling when it improves implementation quality, documentation clarity, test coverage, or maintenance efficiency without displacing accountable human review.

AI output is treated as an untrusted contribution until a maintainer verifies it against repository authority, security requirements, schemas, tests, and documentation standards.

## Permitted uses

AI-assisted tooling may be used to:

- draft or refine documentation, examples, tests, and implementation code
- identify inconsistencies, missing validation, or possible defects
- propose diagrams, crosswalks, and machine-readable artefacts
- assist with dependency maintenance and refactoring

## Required controls

Any AI-assisted change must satisfy the same acceptance gates as a human-authored change:

1. **Authority:** normative behaviour must remain traceable to the governing specification, profile, schema, or approved repository decision.
2. **Verification:** generated code and artefacts must pass the repository validation and test suites.
3. **Security:** secrets, private data, unpublished vulnerability details, and restricted third-party material must not be submitted to external AI services.
4. **Licensing:** contributors must verify that proposed content is compatible with the repository licence and does not reproduce protected material without permission.
5. **Review:** a human contributor remains responsible for correctness, provenance, and the final commit.
6. **Disclosure:** material AI assistance should be disclosed in the pull request description when it materially shaped code, tests, documentation, or architecture.

## Prohibited uses

AI output must not be merged solely because it is syntactically valid or persuasive. It must not be used to fabricate test evidence, citations, conformance claims, security review, provenance, or maintainer approval.

## Evidence expectations

A pull request containing material AI-assisted work should identify:

- the affected files or work products
- the human validation performed
- the commands and tests executed
- any unresolved limitations or assumptions

The pull request template provides a disclosure field for this purpose.

## Accountability

The contributor and approving maintainer retain responsibility for every merged change. AI systems have no authority to approve, waive, revoke, or reinterpret repository requirements.
