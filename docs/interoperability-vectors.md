# Interoperability Vectors

## Included vectors

This repository includes example vectors for:

- standard verification
- gateway-mediated verification
- multi-authority gateway routing
- benchmark-style request payloads

## Canonical fixture exchange

`v0.13.0` adds a more structured exchange surface for interoperability work:

- `fixtures/profile-bound/standard-v1/`

That package gives another implementation everything it needs to replay a known-good case with pinned inputs.

## What should stay stable across implementations

- resolved profile semantics
- trust outcome
- transport evaluation result
- revocation freshness evaluation result
- replay contract expectations
