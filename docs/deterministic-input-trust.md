# Deterministic Input Trust

## Why this release exists

A verifier can be perfectly consistent in how it applies policy and still be weak in practice if it cannot account for the quality of the inputs it trusted while making that decision.

That is the gap `v0.13.0` addresses.

The core move in this release is simple: the verifier now treats feed transport, revocation freshness, and replay evidence as part of the control plane rather than as implementation detail.

## What changed

### Transport is now governed

Verification profiles can now declare the kind of feed path they are willing to trust.

This includes:

- whether the verifier expects local data, direct HTTP, or gateway mediation
- what integrity posture is acceptable
- whether feed availability is optional or mandatory

The verifier records both the **required** and the **actual** transport posture in exported evidence.

### Revocation freshness is now explicit

Revocation handling is no longer just a boolean check against a feed.

Profiles now state:

- how old revocation material may be
- whether stale material causes warning or failure
- whether delta/live channel semantics are required

This creates a machine-verifiable line between “the verifier had revocation data” and “the verifier had revocation data fresh enough to matter.”

### Replay now carries input trust context

Replay bundles now include:

- transport metadata
- revocation status
- a replay contract showing whether transport checks passed and whether revocation freshness was evaluated

That improves portability across implementations because the question is no longer only “did the same request yield the same result?” It is also “was the same input trust posture asserted and evidenced?”

## Why this matters for assurance

This repository has always aimed to show that TRQP can function as a governance decision plane for verification workflows.

A decision plane needs more than decision logic. It also needs evidence about the decision environment.

Without that, the system can produce a decision receipt that looks complete while leaving a critical question unanswered: **what did the verifier assume about the reliability of its own policy inputs?**

## Practical impact

For implementers, `v0.13.0` makes four things easier:

1. expressing different transport assumptions without rewriting verifier logic
2. testing stale or degraded revocation paths explicitly
3. exchanging canonical fixtures with other implementations
4. exporting evidence that is more credible during audit, interoperability testing, and governance review

## Boundary of this release

This release does not try to solve full transport attestation or production-grade policy distribution.

It creates a clean and testable control surface for those next steps.

That is the right increment. It turns a roadmap topic into something executable, inspectable, and extensible.
