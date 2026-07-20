---
layout: default
title: "API Call Catalogue"
description: "Complete implemented call surface, request/response contracts, errors, and review ownership."
parent: "Implementation Guides"
nav_order: 3
---
# API Call Catalogue

This catalogue is the human-readable index of every network call implemented by the reference service. The machine-readable source is [`api/openapi.json`](../api/openapi.json).

## Complete operation inventory

| Operation ID | Method and path | Caller | Input | Output | Governance purpose |
|---|---|---|---|---|---|
| `getHealth` | `GET /health` | Operator, orchestrator | None | Health and capability declaration | Makes deployed capability visible |
| `queryAuthorization` | `POST /trqp/authorization` | Verifier or relying service | Authorization request | Authorization response | Tests whether an entity may perform an action on a resource under an authority |
| `queryRecognition` | `POST /trqp/recognition` | Verifier or relying service | Recognition request | Recognition response | Tests whether one authority recognizes another |
| `queryGatewayAuthorization` | `POST /trqp/gateway/authorization` | Verifier using mediation | Authorization request | Authorization response plus gateway mediation evidence | Preserves delegation and route evidence |
| `verifyAsset` | `POST /trqp/verify` | CAWG/C2PA verifier integration | Verification request plus profile controls | Verification result | Synthesizes integrity, recognition, authorization, process, freshness, and gateway evidence |
| `exportAuditBundle` | `POST /trqp/audit-bundle` | Auditor, verifier, assurance system | Same request as verification | Audit bundle | Produces replayable decision evidence |

## Common transport rules

- Content type for every `POST` operation: `application/json`.
- Maximum request body: 65,536 bytes.
- Request bodies must be JSON objects.
- Unknown top-level controls are ignored by `/trqp/verify` and `/trqp/audit-bundle` unless included in the explicit request/control set; direct authorization schemas disallow additional properties.
- Invalid transport or shape returns a structured error and does not perform a policy decision.
- A policy denial, failed recognition, or untrusted verification is a successful HTTP exchange with a negative domain outcome.

## 1. Health

### Request

```http
GET /health
```

### Response `200`

```json
{
  "status": "healthy",
  "capabilities": ["authorization", "recognition", "verify", "audit_bundle", "gateway"]
}
```

## 2. Authorization query

### Request `POST /trqp/authorization`

| Attribute | Requirement | Type | Description |
|---|---|---|---|
| `entity_id` | Mandatory | string | Entity whose delegated or direct authority is queried |
| `authority_id` | Mandatory | string | Authority governing the decision scope |
| `action` | Mandatory | string | Requested action |
| `resource` | Mandatory | string | Resource or resource class |
| `context` | Optional | object | Deterministically normalized contextual constraints |

### Response `200`

| Attribute | Requirement | Type | Description |
|---|---|---|---|
| `authorized` | Mandatory | boolean | Authorization outcome |
| `expires` | Optional | string | Decision expiry timestamp |
| `policy_epoch` | Optional | string | Policy state identifier |
| `evidence` | Optional | array of strings | Evidence references |
| `reason` | Optional | string | Machine-readable or implementation-defined reason |
| `policy_requirements` | Optional | object | Requirements attached to the authorization |

## 3. Recognition query

### Request `POST /trqp/recognition`

| Attribute | Requirement | Type | Description |
|---|---|---|---|
| `authority_id` | Mandatory | string | Authority whose recognition policy is queried |
| `recognized_authority_id` | Mandatory | string | Candidate authority or issuer to recognize |
| `context` | Optional | object | Recognition scope and constraints |

### Response `200`

The response mirrors authorization structure with `recognized` as the mandatory boolean instead of `authorized`.

## 4. Gateway authorization query

### Request

Same fields as the authorization query.

### Response `200`

```json
{
  "authorization": {
    "authorized": true,
    "policy_epoch": "2026-07-01"
  },
  "gateway_mediation": {
    "gateway_id": "gateway:http",
    "route_label": "http-pattern",
    "authority_id": "urn:trqp:authority:example",
    "decision_type": "authorization",
    "route_attested": false
  }
}
```

The mediation object is evidence of the selected delegation route. It is not a substitute for the underlying authorization response.

## 5. Verification

### Request `POST /trqp/verify`

The domain fields and CAWG mappings are defined in the [CAWG Input Contract](cawg-input-contract.md). The operation additionally accepts:

| Attribute | Requirement | Type | Default | Description |
|---|---|---|---|---|
| `profile` | Optional | string or object | `standard` | Built-in profile name or inline profile payload |
| `overlays` | Optional | array of strings | `[]` | Built-in profile overlays |
| `use_gateway` | Optional | boolean | `false` | Route policy calls through the trust gateway |

### Response `200`

| Attribute | Type | Meaning |
|---|---|---|
| `asset_integrity` | string | Manifest/asset integrity appraisal |
| `assertion_binding` | string | Binding between assertions and asset |
| `issuer_recognition` | string | Recognition outcome |
| `actor_authorization` | string | Authorization outcome |
| `process_integrity` | string | Process evidence outcome |
| `policy_freshness` | string | Freshness posture |
| `verification_mode` | string | Online, cached, gateway, or edge mode |
| `trust_outcome` | string | Synthesized relying-party outcome |
| `process_appraisal` | object | Structured process evidence appraisal |
| `policy_evidence` | object | Policy, revocation, descriptor, and query evidence |
| `gateway_mediation` | object | Route evidence when a gateway is used |
| `explanations` | array of strings | Human-readable diagnostic explanations |

## 6. Audit-bundle export

`POST /trqp/audit-bundle` accepts the same request and controls as `/trqp/verify`. It performs verification and returns the schema-backed audit bundle defined in the [Audit Bundle Profile](audit-bundle-profile.md). The bundle preserves request summary, profile, result, input references, and replay material.

## Error envelope

| Status | Error code | Trigger |
|---|---|---|
| `400` | `invalid_request` | Missing/invalid fields, invalid profile, non-object JSON |
| `413` | `request_too_large` | Body exceeds 65,536 bytes |
| `415` | `invalid_request` | Content type is not `application/json` |

```json
{
  "error": "invalid_request",
  "message": "Missing fields: asset_id, action"
}
```

## Call-to-spec review matrix

| Call | Primary review owner | Questions exposed |
|---|---|---|
| Authorization | TRQP | Are subject, action, resource, context, expiry, evidence, and reason semantics sufficiently specified? |
| Recognition | TRQP | Is issuer/authority recognition scoped and distinguishable from authorization? |
| CAWG input mapping | CAWG/C2PA + integration profile | Are actor, issuer, action, process evidence, and integrity validation exported in interoperable form? |
| Verification synthesis | Joint profile | Which combinations of CAWG evidence and TRQP outcomes produce a relying-party result? |
| Gateway mediation | TRQP/deployment profile | How are delegated routes identified, attested, revoked, and audited? |
| Audit bundle | Joint assurance work | Which evidence must be retained for independent replay and conformance? |

## Machine-verifiable artifacts

- `api/openapi.json`: complete operation contract.
- `schemas/*.schema.json`: payload contracts.
- `examples/api/*.json`: canonical request/response examples.
- `scripts/validate_api_contract.py`: contract consistency gate.
- `tests/test_api_contract.py`: CI-visible contract tests.
