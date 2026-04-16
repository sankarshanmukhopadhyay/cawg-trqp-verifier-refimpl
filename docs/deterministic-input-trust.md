# Deterministic Input Trust

## Why this exists

A verifier can be perfectly consistent in how it applies policy and still be weak in practice if it cannot account for the quality of the inputs it trusted while making that decision.

That is the gap the deterministic input trust work addresses.

The core move is simple: the verifier now treats feed transport, revocation freshness, and replay evidence as part of the control plane rather than as implementation detail.

## Transport is governed

Verification profiles can declare the kind of feed path they are willing to trust.

This includes:

- whether the verifier expects local data, direct HTTP, or gateway mediation
- what integrity posture is acceptable
- whether feed availability is optional or mandatory

The verifier records both the required and the actual transport posture in exported evidence.

## Revocation freshness is explicit

Revocation handling is no longer just a boolean check against a feed.

Profiles now state:

- how old revocation material may be
- whether stale material causes warning or failure
- whether delta or live channel semantics are required

This creates a machine-verifiable line between “the verifier had revocation data” and “the verifier had revocation data fresh enough to matter.”

## Replay carries input-trust context

Replay bundles now include transport metadata, revocation status, and a replay contract showing whether transport checks passed and whether revocation freshness was evaluated.

That improves portability across implementations because the question is no longer only “did the same request yield the same result?” It is also “was the same input-trust posture asserted and evidenced?”

## Interoperability impact

The next step after deterministic input trust is interoperability fidelity. That is why the repository now also publishes canonical fixture packages and a compatibility matrix. These artifacts give another implementation a concrete way to test whether it preserves the same trust semantics under standard, high-assurance, gateway-mediated, and multi-authority conditions.

## Practical impact

For implementers and governance teams, this work makes five things easier:

1. expressing different transport assumptions without rewriting verifier logic
2. testing stale or degraded revocation paths explicitly
3. exporting evidence that is credible during audit and governance review
4. exchanging canonical fixtures with other implementations
5. declaring covered behavior through a machine-readable compatibility artifact

## Boundary of this work

This repository still does not claim full transport attestation or production-grade policy distribution.

What it does provide is a clean, testable control surface that can support those next steps without forcing a redesign.
