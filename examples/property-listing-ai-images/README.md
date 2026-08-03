# AI-Assisted Property Listing Images Example

This example demonstrates how a property marketplace can combine CAWG/C2PA provenance with TRQP authority and policy checks when a realtor uses AI-generated or AI-edited images in a property listing.

The example does **not** claim that provenance proves the physical condition of a property. It shows how the relying party can verify who submitted the image, whether that actor is authorized to market the property, what transformations were declared, which listing policy applies, and what evidence must be retained for review or redress.

## Files

- `listing-submission.json` — normalized submission and provenance facts.
- `listing-policy.json` — marketplace policy and authority requirements.
- `decision-receipt.json` — replayable decision showing a conditional acceptance with mandatory disclosure.

## Expected outcome

The listing is accepted only with a prominent AI-edit disclosure because the image contains generative staging. The receipt preserves the realtor's authority, the seller mandate, the declared transformation, and the marketplace's enforcement decision. Undeclared structural alteration, missing authority, revoked mandates, or absent source bindings must fail closed or be routed to manual review.
