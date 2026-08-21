---
layout: default
title: "HTTP to Audit Bundle Adoption Journey"
description: "Integrate the verifier as a service, preserve the governed decision boundary, and export replayable evidence."
parent: "Implementation Guides"
nav_order: 8
---
# HTTP to Audit Bundle Adoption Journey

This guide is the production-style path from a relying application's first HTTP call to a portable, replayable assurance artifact. It is intended for teams that have moved beyond the CLI quickstart and need to understand the operational contract of running the verifier as a service.

The journey is deliberately evidence-first. An integration is not complete because `POST /trqp/verify` returns HTTP `200`. It is complete when the relying system can show **what was evaluated, under which authority and policy state, why the outcome occurred, what evidence was retained, and whether the decision can be independently replayed**.

## Adoption outcome

At the end of this journey, an adopter should be able to demonstrate the following chain:

```text
service health
  -> request construction
  -> bounded verification
  -> negative/uncertain outcome handling
  -> audit-bundle export
  -> bundle validation
  -> replay
  -> correction/supersession
```

Every transition should produce observable evidence. No step should depend on an unrecorded operator assumption.

## 1. Start the HTTP service

Use the repository service launcher with explicit policy and revocation inputs:

```bash
python scripts/start_http_service.py \
  --policy-path data/policies.json \
  --revocation-path data/revocations.json \
  --host 127.0.0.1 \
  --port 5000
```

For a production deployment, treat the policy and revocation sources as governed inputs. Changing them changes the decision environment even when the application payload is identical.

## 2. Verify deployed capability before sending governed work

Call the health endpoint:

```bash
curl -s http://127.0.0.1:5000/health
```

The service should return a capability declaration containing the implemented authorization, recognition, verification, audit-bundle, and gateway surfaces.

The health check answers whether the process is reachable and which capabilities it claims. It does not prove that trust state is current or that a later authorization decision will succeed.

## 3. Construct a verification request from the relying workflow

The canonical endpoint is:

```http
POST /trqp/verify
Content-Type: application/json
```

A relying application should construct the request from the actual workflow boundary rather than from whatever identity attributes happen to be available. At minimum, bind the request to:

- the asset or resource being evaluated;
- the requested action;
- the actor/issuer evidence supplied by the CAWG/C2PA processing path;
- the authority or recognition context required by policy;
- the verification profile; and
- relevant purpose, jurisdiction, channel, or transaction context.

Use the [CAWG Input Contract](cawg-input-contract.md) for field-level mapping and the [API Call Catalogue](api-call-catalogue.md) for the network contract.

## 4. Make the verification call

A local integration can use a canonical example payload:

```bash
curl -s \
  -H 'Content-Type: application/json' \
  --data @examples/verification_request.json \
  http://127.0.0.1:5000/trqp/verify
```

A successful HTTP exchange is not synonymous with an allowed governance result. The application must read the domain outcome.

## 5. Persist the decision surface, not only a boolean

At minimum, retain or forward the following result surfaces according to the selected privacy/retention profile:

| Evidence surface | Why it matters |
|---|---|
| `trust_outcome` | bounded relying-party disposition |
| `actor_authorization` | separates authorization from identity/recognition |
| `issuer_recognition` | records whether the authority/issuer relationship was accepted |
| `policy_freshness` | exposes whether trust state met freshness requirements |
| `verification_mode` | records online, cached, gateway, or edge posture |
| `policy_evidence` | pins policy, revocation, descriptor, and query evidence |
| `gateway_mediation` | preserves route evidence where mediation is used |
| `explanations` | supplies operator-facing diagnostic context |

Do not reduce this surface to `verified=true`. That destroys the distinction between authority, scope, freshness, recognition, and evidence quality.

## 6. Handle all outcome classes explicitly

The relying system should have an explicit disposition for each class:

| Outcome class | Required integration behavior |
|---|---|
| positive/allow | continue only within the evaluated scope |
| deny | stop the requested governed action and retain the reason/evidence reference |
| indeterminate | do not silently convert missing/stale evidence into permission |
| review | route to the accountable institutional control and preserve conflict evidence |

A production integration should make `deny`, `indeterminate`, and `review` first-class business states. Treating them as generic exceptions makes the governance model non-auditable.

## 7. Export the same decision as an audit bundle

Use the audit-bundle endpoint with the same request and profile controls:

```bash
curl -s \
  -H 'Content-Type: application/json' \
  --data @examples/verification_request.json \
  http://127.0.0.1:5000/trqp/audit-bundle \
  > /tmp/cawg-trqp-audit-bundle.json
```

The audit bundle is the portable evidence boundary. It is useful when the verifier and the later auditor are not the same process, organization, or point in time.

## 8. Validate exported evidence

The repository ships a canonical signed audit bundle. Validate it with the configured trust anchors:

```bash
python scripts/validate_audit_bundle.py \
  examples/exported_audit_bundle.signed.json \
  --trust-anchors data/trust_anchors.json
```

For an adopter-generated bundle, apply the corresponding validation process before treating the artifact as suitable for downstream audit or replay.

Validation should establish structural correctness, expected integrity/signature evidence, and the evidence references required by the selected assurance contract. It does not reclassify the underlying business decision as factual truth.

## 9. Replay the preserved decision

The canonical replay command is:

```bash
python scripts/replay_audit_bundle.py \
  examples/reproducibility_bundle_standard.json \
  --trusted-root .
```

Replay should use preserved state. Do not query current policy or revocation state and then claim that the result reproduces the historical decision.

A valid replay result demonstrates that the same pinned inputs and implementation contract yield the same governed outcome and reason surface.

## 10. Prove correction without rewriting history

A production relying system needs a correction path. If authority evidence, provenance metadata, or policy inputs are later corrected:

1. preserve the original decision receipt/bundle;
2. preserve the correction evidence and its authority;
3. re-evaluate the governed action when the workflow requires it;
4. issue a new receipt or bundle; and
5. link the new evidence to the original as superseding rather than destructive.

This is essential for appeals, incident investigation, disputes, and longitudinal assurance.

## Operational acceptance tests

Before calling the service integration production-ready, demonstrate these tests against your deployment:

| Test | Expected evidence |
|---|---|
| health/capability check | capability declaration |
| valid in-scope request | positive governed result with policy evidence |
| wrong action/resource context | explicit scope failure |
| revoked authority | explicit non-positive outcome and revocation evidence |
| stale required policy state | indeterminate/fail-closed posture according to profile |
| authority conflict | review/conflict evidence rather than implicit allow |
| audit-bundle export | portable bundle tied to the evaluated request |
| bundle validation | independent validation result |
| deterministic replay | same outcome for identical pinned inputs |
| corrected evidence | linked superseding decision without erasing the original |

## Evidence an adopter should retain

A minimal integration evidence set should contain:

- deployment/version identifier;
- selected verification profile and overlays;
- request context sufficient to reconstruct the governed boundary;
- result and stable reason surface;
- policy, authority, recognition, revocation, and descriptor references;
- decision time and freshness evidence;
- audit-bundle identifier or artifact;
- replay result/reference; and
- correction or challenge lineage when applicable.

## Authority and responsibility boundary

The verifier determines whether configured provenance, authority, scope, policy, and trust-state conditions are satisfied. The relying organization remains authoritative for the substantive consequence of that result.

For example, an `allow` may permit authenticated media to enter an editorial, legal, medical, public-safety, or commercial workflow. It does not decide truth, liability, admissibility, diagnosis, safety, or entitlement.

## What can be tested

Run the repository's complete gate before adopting examples or contracts from a particular commit:

```bash
make validate
```

The API-specific contract can be checked with:

```bash
python scripts/validate_api_contract.py
pytest -q tests/test_api_contract.py
```

Replay and audit evidence can be checked independently with the commands above. This gives adopters a layered evidence model rather than one opaque integration test.

## Next journey

Once the positive path works, continue with [Operational Failure, Correction, and Redress](operational-failure-correction-redress.md). Production assurance is defined as much by how the integration behaves when authority is revoked, evidence becomes stale, or a decision is contested as by its happy path.
