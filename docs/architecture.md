# Architecture

## Architectural positioning

TRQP is the **governance decision plane** in the verification workflow.

| Plane | Responsibility |
|---|---|
| Content plane | CAWG/C2PA manifest and assertions |
| Identity plane | Actor and issuer binding |
| Governance plane | Authorization and recognition |
| Decision plane | Final trust outcome synthesis |

## Invocation point

TRQP is invoked **after identity extraction** and **before final decision synthesis**.

## Query unit

The primary query unit is:

`(entity_id, authority_id, action, resource, context)`

This supports tuple-level caching and reuse across many assets from the same entities.
