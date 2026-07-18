---
layout: default
title: "Monday Presentation Brief"
description: "A ten-minute walkthrough of this repository for the CAWG member presentation."
nav_order: 4
---

# Monday Presentation Brief
{: .fs-9 }

A ten-minute, live-demoable walkthrough of `cawg-trqp-verifier-refimpl` for
a CAWG member audience. This page is a speaker aid, not a substitute for the
underlying docs — every claim below links to the page that backs it.
{: .fs-6 .fw-300 }

---

## Framing (60 seconds)

CAWG/C2PA give you **assertions** about content: who made it, what process
produced it, what authority stands behind it. Assertions alone don't answer
the question a relying party actually has: *should I trust this, and can I
defend that decision later?*

This repository is a reference implementation of the layer that answers
that question — using **TRQP** (Trust Registry Query Protocol) as the
authority-query mechanism — and it produces evidence that survives scrutiny:
a structured decision receipt and a replayable audit bundle, not just an
allow/deny flag.

**One line to remember:** *it doesn't just decide — it shows its work, and
lets someone else check the work independently.*

## Live demo (3–4 minutes)

Run these three commands in order. Each maps to one claim on this page.

```bash
# 1. A standard verification decision
python -m cawg_trqp_refimpl.cli examples/verification_request.json --profile standard
```

```bash
# 2. The same request, but fail-closed / high-assurance, with signed feed evidence
python -m cawg_trqp_refimpl.cli examples/verification_request.json \
  --profile high_assurance \
  --policy-descriptor examples/feed_descriptors/policy-feed.signed.json \
  --revocation-descriptor examples/feed_descriptors/revocation-feed.signed.json
```

```bash
# 3. Independently replay a canonical decision from pinned inputs and confirm it matches
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
```

Talking points while it runs:

- Command 1 shows a normal decision — note the `trust_outcome`, `process_appraisal`,
  and `policy_evidence` fields. This is the [Decision Receipt](decision-receipt-specification.md).
- Command 2 shows the *same* request evaluated under a stricter profile that requires cryptographically signed policy and revocation feeds and fails closed if they're missing or invalid — see [Verifier Profiles](verifier-profiles.md) and [Descriptor Policy](descriptor-policy.md).
- Command 3 is the key credibility point: a **third party**, with no access to the live verifier, can re-derive the same decision from pinned inputs and get `"matches": true`. See [Reproducibility Guide](reproducibility-guide.md).

If live execution isn't possible in the room, screenshot the three outputs
in advance — the `matches: true` field in command 3's output is the single
most important thing to have visible.

## The four things to land (4–5 minutes)

1. **It's a governance decision, not a lookup.** The profile encodes policy — who has authority, how fresh revocation data must be, what transport posture is required, whether to fail open or closed. See [Architecture](architecture.md).

2. **Authority is queried, not assumed.** Authorization and recognition are live TRQP-style lookups against a policy source, with the specific evidence recorded — `registry-entry:...`, `trust-list:...` — not a boolean. See [How TRQP Enables Assurance](how-trqp-enables-assurance.md).

3. **Evidence is exportable and independently checkable.** The audit bundle is a signed, schema-backed artifact anyone can replay. This is what turns "trust us" into "verify us." See [Audit Bundle Profile](audit-bundle-profile.md).

4. **It's built for interoperability, not lock-in.** A published compatibility matrix and canonical fixture packages let other implementations prove they preserve the same decision semantics. See [Interoperability Vectors](interoperability-vectors.md) and [Compatibility Matrix](compatibility-matrix.md).

## Anticipated questions

| Question | Short answer | Detail |
|---|---|---|
| Does this replace the TRQP spec or CAWG/C2PA standards? | No — it implements against them and is explicitly not authoritative over them. | [Governance](../GOVERNANCE.md) |
| Is this production-ready? | It's a reference implementation, Beta stability, with a real CI/test gate (68/68 passing) and hardened HTTP surface — suitable for piloting and conformance work, not yet a claimed production SLA. | [Release Readiness](release-readiness.md) |
| Can another team's verifier be checked against this one? | Yes — via the compatibility matrix and canonical fixture packages, and the assurance-suite ingestion manifest for external conformance programs. | [Assurance Suite Ingestion](assurance-suite-ingestion.md) |
| What happens if policy or revocation data is stale or unavailable? | Behavior is profile-controlled and explicit — `standard` can fail open, `high_assurance` fails closed — and the decision receipt records which happened. | [Descriptor Policy](descriptor-policy.md) |
| Does it handle real (binary) C2PA manifests today? | Not yet — there's a stable parser-adapter boundary reserved for a binary backend; today's fixtures are JSON-form manifests. This is the top roadmap item. | [Parser Adapter Contract](parser-adapter-contract.md), [Roadmap](../ROADMAP.md) |
| Where does this fit relative to the rest of the TRQP ecosystem? | It's the reference-implementation stage in a five-stage adoption path: protocol → security profile → reference implementation → conformance suite → assurance hub. | [TRQP Adoption Path](trqp-adoption-path.md) |

## Closing line

*"This repository doesn't just tell you whether to trust a piece of
content — it tells you why, and it lets someone who wasn't in the room
check that reasoning for themselves."*

## One-slide summary (if you need a visual)

```text
CAWG/C2PA assertions
        │
        ▼
 Verification profile (policy: authority, freshness, revocation, transport)
        │
        ▼
 TRQP authority query  ──►  Process appraisal  ──►  Decision
        │
        ▼
 Decision receipt  +  Audit bundle  ──►  Independently replayable
```
