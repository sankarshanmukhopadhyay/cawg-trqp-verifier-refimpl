---
layout: default
title: "Agentic AI Assurance"
nav_order: 10
has_children: true
description: "A cross-cutting assurance model for agents acting as producers, submitters, verifiers, orchestrators, or decision actors."
---
# Agentic AI Assurance

Agentic AI changes the walkthrough problem from *who produced this content?* to *which actor performed this action, for which principal, under what mandate, within what scope, and with what evidence?* This section extends the CAWG-TRQP walkthrough model so that content provenance, actor authority, delegated action, verification, and downstream institutional accountability remain separable and testable.

The governing rule is simple: **agent identity is not agent authority**. A verifier must be able to distinguish an authenticated agent from an authorized agent, and an authorized agent from an agent authorized for the specific action, resource, purpose, jurisdiction, and decision time being evaluated.

## Assurance stack

```mermaid
flowchart TB
    A[Institutional decision or action] --> B[Agent task and mandate]
    B --> C[Authority and delegation evidence]
    C --> D[TRQP recognition and authorization]
    D --> E[Content provenance and transformation evidence]
    E --> F[Source artefact or event]
```

The stack preserves three independent questions:

1. **Content assurance:** what happened to the artefact?
2. **Actor and authority assurance:** who acted, for whom, and under what authority?
3. **Action and decision assurance:** was the action within mandate, and can it be reviewed, corrected, revoked, or appealed?

## Agent roles

An agent can appear in one or more roles without gaining authority from another role automatically:

| Role | Typical action | Assurance question |
|---|---|---|
| Producer | Generates or transforms content | Was this agent authorized to create or alter this artefact under the applicable transformation policy? |
| Submitter | Packages or submits evidence | Was this agent authorized by the principal to submit this resource to this recipient for this purpose? |
| Verifier | Resolves provenance, authority, or policy state | Was the agent authorized to perform verification, and are its findings reproducible from pinned evidence? |
| Orchestrator | Calls registries, tools, verifiers, or other agents | Can the full delegated action chain be reconstructed and bounded? |
| Decision agent | Recommends or executes a downstream action | Was the agent separately delegated decision authority, and are escalation/redress controls preserved? |
| Proxy | Acts on behalf of a human or organization | Is the principal-agent relationship current, scoped, and revocable? |

## Core documents

- [Agent Role Model](agent-role-model.md)
- [Delegation and Authority](delegation-and-authority.md)
- [Delegated Creator TRQP Traceability](delegated-creator-trqp-traceability.md) (informative taskforce gap analysis)
- [Experimental Delegated Creator Profile](experimental-delegated-creator-profile.md) (versioned local feasibility experiment)
- [Taskforce Five-World Demonstration](taskforce-five-world-demo.md) (portable synthetic vectors and eight-test assessment)
- [Verification and Decision Boundaries](agentic-verification-boundaries.md)
- [Agentic Walkthrough Pattern](agentic-walkthrough-pattern.md)

## Experimental Delegated Creator path (v0.20.0)

The [v0.20.0 release](../../RELEASE_NOTES_v0.20.0.md) adds **repository-local,
non-normative** experiments. To evaluate them without implying verified
CAWG/C2PA interoperability:

1. Start with the [five-world demonstration](taskforce-five-world-demo.md) to export a deterministic synthetic decision report, compare expected and actual outcomes, and inspect separate historical/current and assured result fields.
2. Run the [Session 2 scenarios](../../tests/test_taskforce_session2_scenarios.py) for human manager delegation, pseudonymous uniqueness claims and professional vouching; examine the [scenario catalogue](../../conformance/delegated-creator-session2-scenarios.json).
3. Review the [enterprise-binding negative tests](../../tests/test_enterprise_binding_assurance.py) and [assurance traceability](delegated-creator-trqp-traceability.md) to understand why a valid signature or credential claim does not establish authority to act for an organization.

```bash
python scripts/run_taskforce_five_world_demo.py --output /tmp/taskforce-report.json
pytest -q tests/test_taskforce_session2_scenarios.py tests/test_enterprise_binding_assurance.py
```

The five-world report's `assured_authority` and `assured_coverage` remain
non-positive. This path is a testable feasibility demonstration, **not** proof
of accepted CAWG delegation assertions, issuer trust or independent TRQP
interoperability. External evidence remains tracked in [issue #75](https://github.com/sankarshanmukhopadhyay/cawg-trqp-verifier-refimpl/issues/75).

## Executable archetypes

The walkthrough portfolio includes three machine-readable agentic archetypes:

- [Agent as Content Producer](../workflows/agent-content-producer.md)
- [Agent as Delegated Submitter](../workflows/agent-delegated-submitter.md)
- [Agent as Verifier and Orchestrator](../workflows/agent-verifier-orchestrator.md)

These archetypes are intentionally cross-sector. Sector walkthroughs reuse the same controls through their **Agentic AI Variant** sections.
