# Architecture

## Architectural positioning

TRQP remains the **governance decision plane** in the verification workflow, but v0.7.0 adds a process appraisal layer that lets the verifier reason about how a claimed action was carried out.

| Plane | Responsibility |
|---|---|
| Content plane | CAWG/C2PA manifest and assertions |
| Identity plane | Actor and issuer binding |
| Governance plane | Authorization and recognition |
| Process plane | Process evidence and appraisal |
| Decision plane | Final trust outcome synthesis |

## Invocation point

TRQP is invoked **after identity extraction** and **before final decision synthesis**.

The process appraisal layer is invoked after policy retrieval so that policy can declare whether process proof is required and what minimum integrity threshold applies.

## Query unit

The primary query unit is:

`(entity_id, authority_id, action, resource, context)`

This supports tuple-level caching and reuse across many assets from the same entities.

## Composite decision model

The effective trust decision now depends on three distinct questions:

1. Is the asset integrity-valid?
2. Is the actor authorized and issuer recognized under TRQP-governed policy?
3. Does the supplied process evidence satisfy the policy requirements attached to that authorization path?

That makes the verifier more expressive without collapsing responsibilities between governance and evidence systems.
