---
layout: default
title: "Operator Decision and Replay Walkthrough"
description: "Run a verification, inspect the governed decision surface, and replay the evidence deterministically."
parent: "Assurance & Evidence"
nav_order: 8
---
# Operator Decision and Replay Walkthrough

This walkthrough connects the repository's quickstart, decision receipts, audit evidence, and replay tooling into one operator-facing flow. It is intentionally sector-neutral: the objective is to show what an implementer can run, what evidence is created, what each evidence surface means, and how the same decision can be replayed without silently substituting current state for historical state.

The central governance question is not simply **"did verification pass?"** It is:

> **Which actor was allowed, denied, or routed to review for which action, on which resource, under which policy and trust state, and can another operator reproduce that conclusion from preserved evidence?**

A positive result is a bounded authorization outcome. It is not proof of factual truth, ownership, editorial accuracy, clinical validity, legal admissibility, or any other downstream substantive judgment.

## 1. Install the reference implementation

Create an isolated environment and install the pinned dependencies:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-lock.txt
pip install -e .
```

The lock file is part of the reproducibility boundary. An operator evaluating historical evidence should avoid treating a materially different dependency set as equivalent unless the change has been separately assessed.

## 2. Run the canonical verification request

Execute the repository's canonical request under the `standard` profile:

```bash
python -m cawg_trqp_refimpl.cli examples/verification_request.json --profile standard
```

The structured result is the first evidence surface. Read it as a governed decision record rather than a generic validity flag. At minimum, an operator should be able to identify:

| Question | Evidence to locate |
|---|---|
| What action was evaluated? | requested action / normalized request context |
| Which resource was in scope? | resource identifier and contextual bindings |
| Which actor or authority path was evaluated? | authority and delegation evidence |
| Which policy applied? | policy/profile identifiers and epoch/version references |
| Was revocation evaluated? | revocation state and freshness evidence |
| What was the outcome? | decision/disposition and stable reason code |
| When was the decision made? | decision time |
| Can the decision be reproduced? | pinned inputs, receipt, bundle, or replay references |

The important implementation property is separation. Content-authenticity evidence can establish facts about provenance and assertions carried with an asset. TRQP-governed evidence can establish whether a recognized actor was authorized for the requested action and context. The relying organization still owns the downstream decision.

## 3. Change the assurance profile deliberately

The repository defines three primary verification profiles:

- `standard` for online or cache-assisted verification;
- `high_assurance` for consequential decisions that require current governed evidence; and
- `edge` for offline or intermittently connected operation where staleness must remain visible.

Run the same class of request under a different profile only when the relying workflow has explicitly selected that assurance posture. A profile is not a performance preset. It changes the evidence and failure contract.

For high-assurance processing, stale or defective required trust-state evidence must not be converted into an implicit allow. For edge processing, use of a governed snapshot is acceptable only when the decision surface exposes the snapshot and staleness conditions that constrained the result.

## 4. Inspect the decision boundary before the reason code

A reason code is meaningful only inside the requested action and scope. Before interpreting `AUTHORIZED`, `SCOPE_MISMATCH`, `AUTHORITY_REVOKED`, `TRUST_STATE_STALE`, or `AUTHORITY_CONFLICT`, verify that the request is bound to the intended:

1. actor or authority path;
2. action;
3. resource;
4. purpose or relying context where applicable;
5. jurisdiction/location where policy requires it; and
6. evaluated decision time.

This prevents a common governance failure: taking evidence that is valid for one operation and treating it as portable authorization for another. Recognition is not authorization, and authorization for one resource or purpose is not universal delegation.

## 5. Read negative and uncertain outcomes as evidence

The verifier exposes more than binary pass/fail semantics. An operator should preserve the distinction between:

| Outcome class | Operational meaning |
|---|---|
| `allow` | configured provenance, authority, scope, policy, and trust-state conditions were satisfied |
| `deny` | a material governed condition failed, such as scope or revocation |
| `indeterminate` | required evidence could not be established to the configured assurance level |
| `review` | the machine-verifiable evidence exposes a conflict or condition requiring an institutional decision |

`indeterminate` and `review` are successful governance outcomes when uncertainty is real. They prevent missing or conflicting evidence from being laundered into permission.

## 6. Validate the repository evidence surface

Before relying on the examples as a conformance or adoption aid, run the complete repository gate:

```bash
make validate
```

For narrower inspection, the following checks isolate useful assurance surfaces:

```bash
python scripts/validate_examples.py
python scripts/validate_feed_descriptors.py
python scripts/validate_walkthrough_examples.py
python scripts/validate_walkthrough_quality.py
python scripts/validate_walkthrough_diagrams.py
```

A successful documentation check is not a substitute for semantic verification, but it does prove that the published examples and reader-facing walkthroughs remain linked to the machine-readable scenario portfolio expected by CI.

## 7. Inspect the canonical replay bundle

The repository's canonical replay artifact is:

```text
examples/reproducibility_bundle_standard.json
```

It pins the inputs needed to reconstruct the decision surface, including transport metadata, revocation status, and a replay contract describing which checks were performed. The key governance requirement is that replay evaluates preserved state rather than opportunistically querying today's state and pretending it was the state available at the original decision time.

Check the bundle directly:

```bash
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
```

Then replay it:

```bash
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json
```

For a trust-root constrained replay, use the repository's trusted root where required by the selected flow:

```bash
python scripts/replay_audit_bundle.py \
  examples/reproducibility_bundle_standard.json \
  --trusted-root .
```

## 8. Understand deterministic replay

Replay is useful only if an auditor can distinguish these cases:

- **same pinned inputs, same implementation contract, same outcome**: expected deterministic replay;
- **same historical evidence, newer implementation**: compatibility must be demonstrated rather than assumed;
- **corrected authority or provenance evidence**: generate a new decision and link it to the earlier receipt;
- **new current revocation state**: do not rewrite the historical result; evaluate a new decision when the workflow requires a current-state answer;
- **missing replay input**: fail the replay contract explicitly rather than filling the gap from an unrecorded source.

Historical receipts are evidence of what the governed verifier decided under a recorded state. They are not mutable truth records.

## 9. Validate signed audit evidence

Where a relying workflow exports a signed audit bundle, validate the bundle against the configured trust anchors:

```bash
python scripts/validate_audit_bundle.py \
  examples/exported_audit_bundle.signed.json \
  --trust-anchors data/trust_anchors.json
```

The audit bundle provides a portable boundary around the decision evidence. Signature validation answers whether the bundle satisfies the repository's configured integrity/trust checks. It does not elevate the bundle's underlying claims beyond their original scope.

## 10. Follow correction rather than mutation

Assurance systems need a correction model because authority, metadata, or provenance evidence may later be shown to be wrong. The repository's model is additive:

1. preserve the original receipt and replay inputs;
2. record the corrected material input or authority evidence;
3. evaluate a new decision under the applicable policy and decision time;
4. issue a superseding receipt; and
5. link the new evidence to the prior decision without erasing history.

This creates an auditable lineage for appeal, redress, incident investigation, and longitudinal assurance.

## What can be tested

| Assurance question | Repository evidence |
|---|---|
| Can a canonical request be evaluated? | CLI quickstart request |
| Are authority and scope failures explicit? | stable outcomes and reason codes |
| Does stale/conflicting state remain visible? | `indeterminate` / `review` paths |
| Are walkthrough scenarios machine-discoverable? | `validate_walkthrough_examples.py` |
| Are reader-facing walkthroughs structurally complete? | `validate_walkthrough_quality.py` |
| Can a preserved decision be replayed? | reproducibility bundle and replay scripts |
| Can signed audit evidence be independently checked? | audit-bundle validator + trust anchors |
| Are corrections non-destructive? | superseding receipt/replay lineage contract |
| Does the whole repository meet its declared gate? | `make validate` |

## Evidence produced

An implementation using this operating model should be able to retain or export, as appropriate to the selected profile and privacy policy:

- normalized request context;
- provenance/assertion findings used in the decision;
- authority, delegation, recognition, and revocation evidence references;
- policy and profile identifiers/epochs;
- decision time;
- outcome and stable reason code;
- minimized decision receipt;
- replay inputs or bundle references;
- integrity/signature evidence for exported bundles; and
- correction, challenge, or redress lineage.

## Operator acceptance criteria

A relying organization should not call an integration production-ready merely because the canonical request returns an allow. At minimum, demonstrate that:

1. an in-scope authorization can be reproduced;
2. an out-of-scope request is denied;
3. a revoked authority cannot authorize a new action;
4. stale required evidence produces the configured non-positive posture;
5. conflicting authoritative evidence is preserved and routed rather than flattened;
6. replay of identical pinned inputs returns the same governed outcome and reason code;
7. a correction creates linked superseding evidence rather than overwriting history; and
8. the relying workflow preserves its own responsibility for substantive judgment.

## Where to go next

Use this guide together with:

- [Quickstart](../QUICKSTART.md) for installation and first execution;
- [Decision Receipt Specification](decision-receipt-specification.md) for the receipt contract;
- [Reproducibility Guide](reproducibility-guide.md) for replay artifacts;
- [Audit Bundle Profile](audit-bundle-profile.md) for portable audit evidence;
- [Walkthrough Catalogue](sections/walkthroughs-index.md) for sector-specific assurance boundaries; and
- [API Call Catalogue](api-call-catalogue.md) when integrating the verifier as a service.

The implementation objective is a decision surface that is **bounded, explainable, enforceable, and replayable**. That is the point at which provenance and registry evidence become executable governance rather than detached metadata.
