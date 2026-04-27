# Compatibility Matrix

The machine-readable compatibility matrix lives at `conformance/compatibility-matrix.json`.

Its purpose is to give downstream assurance hubs, conformance suites, and implementation teams a compact statement of what this repository currently covers.

## What the matrix records

- which profiles have canonical fixture packages
- which verification modes are exercised
- which transport and revocation behaviors are covered
- which evidence artifacts can be consumed by external tooling

## Why this matters

A reference implementation becomes more useful when it can declare not only what it does, but also which claims have been exercised and which remain out of scope. The compatibility matrix is a small but important governance artifact because it turns repository content into a machine-readable assurance surface.

## Current highlights

- canonical fixture packages now exist for standard, high assurance, gateway-mediated, and multi-authority cases
- transport and revocation behaviors have explicit evidence references
- the HTTP service surface is part of the compatibility statement rather than an undocumented side path


## v0.14.0 descriptor compatibility surface

| Capability | Status | Evidence |
| --- | --- | --- |
| Signed policy feed descriptor | Supported | `examples/feed_descriptors/policy-feed.signed.json` |
| Signed revocation feed descriptor | Supported | `examples/feed_descriptors/revocation-feed.signed.json` |
| Signed snapshot feed descriptor | Supported | `examples/feed_descriptors/snapshot-feed.signed.json` |
| Signed gateway route descriptor | Supported | `examples/feed_descriptors/gateway-route-feed.signed.json` |
| Runtime descriptor evidence export | Supported | `policy_evidence.feed_descriptors` |
| Replay descriptor evidence preservation | Supported | `replay_inputs.feed_descriptors` |
