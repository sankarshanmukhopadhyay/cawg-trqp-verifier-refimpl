---
layout: default
title: "Documentation Quality Standard"
description: "Testable requirements for complete, consistent, and implementation-ready technical documentation."
parent: "Contributor & Release Guidance"
nav_order: 1
---
# Documentation Quality Standard

## Objective

Documentation in this repository must allow a reader to understand the system, implement or operate it, verify the resulting behaviour, and identify the authority governing each decision. Narrative explanation alone is insufficient where a machine-verifiable artefact, command, schema, fixture, or test can provide stronger evidence.

## Required content model

Each substantive technical document should contain the sections that are relevant to its purpose:

| Concern | Required documentation outcome | Evidence surface |
|---|---|---|
| Purpose and scope | State what the component does and does not do | Scope statement |
| Authority | Identify the specification, profile, schema, or repository decision that governs behaviour | Link or artefact identifier |
| Inputs and outputs | Define accepted inputs, produced outputs, and validation rules | Schema, example, or interface table |
| Processing | Explain the sequence, decisions, and failure paths | Mermaid flow or sequence diagram where useful |
| Security and privacy | Identify trust boundaries, failure posture, sensitive data, and abuse considerations | Threat/control notes and tests |
| Operations | Explain configuration, deployment, observability, recovery, and revocation | Commands and operational evidence |
| Verification | Provide reproducible validation steps and expected results | Test command, fixture, receipt, or bundle |
| Limitations | State unsupported cases and known constraints | Explicit limitations section |

## Style requirements

- Use descriptive headings and concise paragraphs.
- Define specialised terms on first use and use one term consistently for one concept.
- Distinguish normative requirements from examples and implementation guidance.
- Prefer active voice and explicit actors, authorities, inputs, and outputs.
- Use numbered steps for procedures and tables for comparable controls or interfaces.
- Use fenced code blocks with language identifiers.
- Use relative repository links for project content and validate all links before merge.
- Avoid unsupported claims such as “secure,” “compliant,” or “production-ready” without evidence and qualification.
- Do not duplicate normative definitions when a canonical schema or specification can be linked.

## Diagram requirements

A Mermaid diagram should be added when it materially reduces ambiguity in:

- multi-party authority or delegation relationships
- request, decision, replay, or evidence flows
- branching policy decisions and failure modes
- deployment boundaries and trust zones
- lifecycle, revocation, or state transitions

Diagrams supplement rather than replace the surrounding text. Node labels must use repository terminology, and every diagram must remain understandable when rendered in a neutral colour scheme.

## Documentation definition of done

A documentation change is complete when:

1. the intended audience and task are clear;
2. terms and links align with the rest of the repository;
3. commands and examples are executable or explicitly marked illustrative;
4. diagrams render through the GitHub Pages pipeline;
5. affected schemas, examples, tests, and navigation are updated;
6. `make validate` and the Pages build succeed; and
7. the pull request records any material AI assistance.
