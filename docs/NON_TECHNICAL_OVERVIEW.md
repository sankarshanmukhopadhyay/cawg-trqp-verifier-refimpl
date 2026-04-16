# Non-Technical Overview

## What this repository does

This repository demonstrates how a trust decision can be made in a way that is not only automated, but also explainable and testable.

It uses TRQP as the policy decision layer for verifying whether a digital asset, its issuer, and its process evidence should be trusted in a CAWG/C2PA workflow.

## What is new in v0.13.0

Earlier versions focused on the decision itself.

This release focuses on the **quality of the information the decision relied on**.

In plain terms, that means the verifier now asks additional questions such as:

- Where did the policy come from?
- Was that delivery path strong enough for the profile being used?
- Was revocation information fresh enough to matter?
- Can another implementation replay the same decision with the same assumptions?

## Why that matters

Many systems can produce a trusted or rejected result.

Far fewer can show whether the policy and revocation inputs used for that result were themselves governed in a clear and testable way.

This release improves that by making transport expectations, revocation freshness, and replay evidence first-class parts of the verifier.

## What teams can do with it

This makes the repository more useful for:

- architecture teams comparing trust models
- governance teams asking how decisions are evidenced
- interoperability programs running cross-implementation checks
- assurance and audit functions reviewing whether the system failed safely

## Bottom line

The verifier is no longer just showing what decision it produced.

It is getting better at showing **what it trusted while producing that decision**.
