---
layout: default
title: "Delegated Creator TRQP Traceability"
parent: "Agentic AI Assurance"
nav_order: 5
---
# Delegated Creator Taskforce: TRQP profile traceability

**Status:** informative, implementation-side gap analysis. **Not** an adopted CAWG profile, a proposed normative text, or a certification result.

This analysis is based on the CAWG Delegated Creator Taskforce kick-off **recap of 23 October 2026**, circulated **25 October 2026**. Its linked minutes, slides, Padlet and CAWG issue #285/#286 discussions were not supplied as authoritative evidence for this mapping. The recap summarizes intended directions, not approved conformance requirements. See the [machine-readable manifest](../../conformance/delegated-creator-taskforce-traceability.json).

## Separate the two profile axes

- **Domain/application semantics:** the taskforce's potential CAWG-specific restrictions on TRQP (delegator/delegate, consent and rights reference, authority scope, signing-time state, chain provenance, evidence classes and generator responsibilities). These remain subject to CAWG decision.
- **Verification/operational posture:** this repository's existing `standard`, `edge` and `high_assurance` profiles specify freshness, failure, revocation, transport, descriptor policy and replay. They are **not** an upstream-approved domain profile. Do not rename or silently reinterpret them.

## Requirements-to-evidence map

| ID | Recap proposition | Disposition | Existing evidence and material gap |
|---|---|---|---|
| DC-01 | Use cases first, including agentic/non-agentic creative worlds | **Partial** | [Walkthrough catalogue](../sections/walkthroughs-index.md) and [agentic model](index.md) support scenario exploration; no evidence maps these to all five taskforce-defined worlds. |
| DC-02 | Manifest records delegation at signing; full agreement/consent/rights are linked | **Partial** | [Delegation and Authority](delegation-and-authority.md) covers temporal validity; [authorization schema](../../schemas/authorization-request.schema.json) captures actor/action/resource. Neither establishes CAWG manifest bindings or consent-reference semantics. |
| DC-03 | Unverified, delegator-covered, credential-backed coverage | **Missing** | Distinct negative outcomes are described in [delegation guidance](delegation-and-authority.md), but these are not the proposed three coverage levels. Do not map an existing positive authorization decision onto credential-backed coverage. |
| DC-04 | Limit chain depth and duration, trace to original consenting party | **Partial** | [Delegation tuple](delegation-and-authority.md) names principal, validity and depth. Taskforce-specific numeric limits, recursive chain proofs, root-consent binding and conformance fixtures are not established. |
| DC-05 | Claim generator witnesses/rejects as a third signer | **Missing** | [Agent role model](index.md) establishes actor-role separation, not a normative third-signature or rejection requirement. |
| DC-06 | Narrow CAWG profile of general TRQP | **Partial** | [Existing profiles](../../profiles/high_assurance.json) and [profile schema](../../schemas/verification-profile.schema.json) constrain **operational assurance**, not CAWG-approved delegated-creator semantics. [Governance](../../GOVERNANCE.md) preserves upstream authority. |
| DC-07 | Survey the impact of unverified authority | **External** | Taskforce discovery/adoption activity. [Repository scenarios](../sections/walkthroughs-index.md) may inform questions but are not survey responses or evidence of industry prevalence. |

Disposition here means **documented evidence of coverage**, not a failed conformance test. “Missing” is not proof no related code exists anywhere; it means the reviewed artifacts do not establish the proposition.

## Bounded implementation and decision sequence

1. **Now:** preserve this seven-point machine-readable traceability baseline and validate its structure/links. This is completed by this documentation tranche, not a change to verifier decisions.
2. **Upstream dependency:** obtain taskforce agreement on the *meaning* of three coverage categories, signing-time evidence binding, the original consenting principal and chain/expiry rules, the responsibilities of the claim generator, and the conformance status of the CAWG TRQP profile. Do not invent mandatory defaults locally.
3. **After semantic agreement:** add a versioned, explicitly provisional CAWG domain profile separate from operational verifier profiles; add valid/invalid fixtures for no vouching, credential-backed evidence, scope mismatch, expired/revoked chain links, depth overflow, conflicting principals and generator rejection. Negative tests must not pass by accepting unknown authority.
4. **Independent review:** run the same fixtures with an independently developed implementation or upstream reference and retain release-pinned evidence. Only CAWG can adopt a CAWG normative profile.

## Reproducible traceability check

```bash
python scripts/validate_delegated_creator_traceability.py
```

This verifies completeness of the seven summarized recap points, status vocabulary, nonempty explanations and valid repository-local evidence paths. It does **not** assert runtime enforcement, interoperability or CAWG conformance.

## Change boundaries

No alteration to published TRQP, CAWG/C2PA standards; no change to production verifier semantics, result schema, CLI/API behaviour, existing operational profiles, or released evidence. No new release is warranted for this analysis alone.
