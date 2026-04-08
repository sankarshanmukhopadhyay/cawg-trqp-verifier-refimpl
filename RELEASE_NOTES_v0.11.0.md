# Release Notes v0.11.0

## Overview

v0.11.0 strengthens the evidence layer of the CAWG–TRQP reference implementation. Exported audit bundles can now be attested, replay can target pinned external policy feeds, and the repository ships with a deterministic reproducibility fixture for cross-run assurance checks.

## Highlights

- optional Ed25519 attestation for audit bundle exports
- bundle validation with trust-anchor verification
- replay portability through pinned policy and revocation feed metadata
- reproducibility fixture and comparison tooling for deterministic regression checks

## Positioning

This increment moves the repository closer to an executable assurance profile. The verifier no longer just emits evidence. It emits evidence that can be signed, validated, replayed, and compared in a disciplined way.
