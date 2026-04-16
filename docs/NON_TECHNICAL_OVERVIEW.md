# Non-Technical Overview

## What this repository does

This repository demonstrates how a trust decision can be made in a way that is not only automated, but also explainable, testable, and portable.

It uses TRQP as the policy decision layer for verifying whether a digital asset, its issuer, and its process evidence should be trusted in a CAWG/C2PA workflow.

## What the current repository state adds

Earlier versions were mainly about reaching a decision and exporting a replayable result.

The current repository state extends that into a more useful public artifact. The project now carries a stronger interoperability surface, not just a stronger verifier.

In practical terms, that means the repository now provides:

- governed transport and revocation expectations inside the profile model
- replay evidence that explains what the verifier trusted while making a decision
- canonical fixture packages that other teams can replay outside this repository
- a machine-readable compatibility matrix showing what the current implementation actually covers
- a documented HTTP service surface that can be exercised as a deployment reference

## Why that matters

Many systems can produce a trusted or rejected result.

Far fewer can show whether the policy and revocation inputs behind that result were governed clearly enough to deserve confidence. Fewer still can hand another implementation a clean package and say, “replay this and show whether you preserve the same semantics.”

That is the shift this repository is making. It is becoming less like a demo and more like an executable handoff artifact.

## Who this helps

This makes the repository more useful for:

- architecture teams comparing trust models and deployment choices
- governance teams asking whether a decision can be explained and contested
- interoperability programs running cross-implementation checks
- assurance and audit functions reviewing whether the system fails safely and reproducibly
- implementers who need a compact starting point for TRQP-aligned verification work

## Bottom line

The verifier is no longer only showing what decision it produced.

It is getting better at showing what it trusted, how that trust was bounded, and how another implementation can test the same claim.
