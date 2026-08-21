---
layout: default
title: "Operational Failure, Correction, and Redress"
description: "Run the verifier safely when authority is revoked, evidence is stale, decisions conflict, or a prior outcome is challenged."
parent: "Implementation Guides"
nav_order: 9
---
# Operational Failure, Correction, and Redress

A production verifier integration is not defined by its successful `allow` path. It is defined by whether the relying system can preserve governance when authority changes, evidence disappears, trust state becomes stale, sources conflict, or an affected party challenges the decision.

This journey turns those conditions into executable operating states. It assumes the adopter has completed the [HTTP to Audit Bundle Adoption Journey](http-to-audit-bundle-adoption-journey.md).

## Operating principle

The system should never make uncertainty disappear merely to keep a workflow moving. The governed states are intentionally distinct:

```text
allow
  |-- later revocation --> new evaluation
  |-- correction -------> superseding evaluation

deny
  |-- correction -------> superseding evaluation

indeterminate
  |-- fresh evidence ---> new evaluation

review
  |-- authoritative resolution --> new evaluation
```

Historical evidence remains immutable. New evidence creates a new governed decision.

## 1. Make failure states explicit in the relying workflow

Map verifier outcomes to business states before deployment. Do not wait for an incident to decide what `indeterminate` or `review` means.

| Verifier state | Relying-system state | Required behavior |
|---|---|---|
| allow | accepted for bounded action | continue only within evaluated scope |
| deny | blocked | prevent action; preserve reason/evidence |
| indeterminate | evidence unavailable/insufficient | hold, retry under governed policy, or escalate |
| review | institutional decision required | queue to named accountable role |

The accountable role for `review` is part of the governance configuration. “Human in the loop” is not sufficient unless the organization can identify who has authority to resolve the conflict and what evidence they must inspect.

## 2. Exercise revocation as an enforcement event

Revocation must change future authorization behavior. The test is not whether the revocation record exists; it is whether the relying action is actually blocked when the configured decision time requires current authority.

A revocation probe should demonstrate:

1. an initially authorized actor/action/resource combination;
2. revocation of the material authority or delegation;
3. a new request after the revocation becomes effective;
4. a non-positive result; and
5. retained evidence identifying the revocation state used by the verifier.

Do not mutate the earlier positive receipt. It remains evidence of the earlier decision environment.

## 3. Exercise stale trust state

Temporarily unavailable or expired authority information must remain visible. A high-assurance profile should not manufacture continuity from stale evidence when current state is required.

Test the configured posture by supplying or simulating trust-state evidence outside its permitted freshness window. The relying system should be able to show:

- which evidence was stale;
- which profile/freshness rule applied;
- the resulting `indeterminate`, `deny`, or other configured fail-closed outcome; and
- what retry or escalation rule was invoked.

The retry path must not silently switch to a weaker profile unless that downgrade is an explicit governance decision.

## 4. Exercise authority conflict

Conflicting authoritative sources are not equivalent to missing data. Preserve the conflict as evidence and route it to the accountable decision authority.

The operator should be able to answer:

- which sources disagreed;
- what each source asserted;
- whether one source has precedence under configured policy;
- which reason code/disposition was emitted; and
- who is authorized to resolve the conflict if policy cannot do so deterministically.

The correct automated result may be `review`. That is a successful assurance outcome when the evidence genuinely conflicts.

## 5. Create a correction record

When a material input is wrong, create a correction rather than editing the historical evidence package.

A correction record should identify:

| Field | Purpose |
|---|---|
| prior decision/bundle identifier | anchors the correction lineage |
| corrected evidence reference | identifies what changed |
| correction authority | identifies who may assert the correction |
| correction time | orders the evidence lifecycle |
| reason | distinguishes error, supersession, withdrawal, or updated state |
| requested re-evaluation | identifies whether a new decision is required |

The correction authority matters. A claimant cannot unilaterally rewrite an authority source merely by submitting new metadata.

## 6. Re-evaluate and issue superseding evidence

Where the correction is material to the decision:

1. construct a new request using the corrected governed inputs;
2. record the applicable policy/profile and decision time;
3. execute verification;
4. export a new receipt/audit bundle; and
5. link the new artifact to the prior decision.

The superseding artifact should not imply that the original decision never occurred. It establishes the current corrected conclusion while preserving the historical audit chain.

## 7. Preserve challenge and redress ownership

A technical verifier can expose evidence and reason codes; it cannot appoint itself as the authority for legal, editorial, clinical, commercial, public-safety, or procedural redress.

An adopter should define at least:

- who may challenge a decision;
- how the challenge references the affected decision/bundle;
- which organization or role receives the challenge;
- what evidence can be corrected or supplemented;
- which authority may resolve conflicts;
- whether the challenged action is paused while review occurs;
- the maximum age/freshness of evidence accepted in review; and
- how the resolution produces a new auditable artifact.

This turns redress from a support process into part of the executable governance model.

## 8. Build an incident evidence packet

When the verifier or its trust inputs contribute to an incident, capture an incident packet before state changes obscure the environment.

At minimum retain:

- request and normalized decision context;
- verifier version/deployment identifier;
- selected profile and overlays;
- policy and descriptor epochs;
- authority/recognition/revocation evidence references;
- decision output and reason surface;
- audit bundle or replay bundle;
- relevant service/configuration change identifiers;
- correction/challenge references; and
- incident disposition owner.

Avoid copying unnecessary personal or sensitive data into an incident packet. Preserve evidence references where the privacy policy permits independent retrieval instead.

## 9. Replay before attributing cause

Use replay to distinguish a deterministic governed outcome from environmental drift.

A useful incident classification is:

| Replay result | Interpretation |
|---|---|
| same pinned inputs, same result | original behavior is reproducible |
| same inputs, different result | implementation/version compatibility issue requires investigation |
| replay impossible due to missing input | evidence-retention failure |
| current-state query differs from historical replay | trust/policy state changed; not itself a replay defect |

Do not substitute a current-state query for replay when investigating what the verifier decided earlier.

## 10. Close the incident with evidence, not only narrative

An incident should be considered governance-closed only when the resolution has machine-verifiable evidence where feasible.

Closure evidence can include:

- superseding decision receipt;
- corrected audit bundle;
- replay result;
- policy/configuration commit identifier;
- revocation/correction reference;
- test that reproduces the former failure mode; and
- accountable owner and disposition reference.

Narrative postmortems are useful, but they are not substitutes for executable regression evidence.

## Conformance probes for adopters

A relying deployment should be able to demonstrate all of these before high-assurance production use:

1. revoked authority blocks a subsequent governed action;
2. stale required evidence cannot yield an implicit positive result;
3. conflicting authority is preserved as conflict and routed correctly;
4. a correction creates a new linked decision rather than rewriting history;
5. an auditor can replay the original decision independently;
6. a challenge has a named receiving authority and evidence reference;
7. the resolution creates a durable evidence artifact; and
8. regression testing prevents the same governance failure from silently recurring.

## Evidence produced

A mature failure/redress implementation produces an evidence chain rather than a ticket trail:

```text
original decision
  -> challenge / incident reference
  -> correction or authoritative resolution
  -> new governed evaluation
  -> superseding receipt/bundle
  -> replay / regression evidence
  -> closure disposition
```

Every arrow represents an auditable transition with an identifiable authority and scope.

## What this journey does not delegate

The verifier does not determine the substantive remedy. It provides evidence about the governed verification decision. The competent relying institution remains responsible for deciding whether the consequence is re-publication, withdrawal, reinstatement, compensation, legal review, clinical review, safety escalation, or another remedy.

## Validation

Use the repository gate to ensure the reference evidence surfaces remain internally consistent:

```bash
make validate
```

Use the audit/replay validators for the evidence lifecycle:

```bash
python scripts/validate_audit_bundle.py \
  examples/exported_audit_bundle.signed.json \
  --trust-anchors data/trust_anchors.json

python scripts/replay_audit_bundle.py \
  examples/reproducibility_bundle_standard.json \
  --trusted-root .
```

The goal is an integration where enforcement, correction, replay, challenge, and closure are all observable governance events rather than undocumented operator judgment.
