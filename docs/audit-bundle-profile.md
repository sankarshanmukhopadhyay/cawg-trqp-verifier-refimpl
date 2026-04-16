# Audit Bundle Profile

## Purpose

The audit bundle captures the verification decision and the evidence needed to replay and examine that decision later.

## v0.13.0 additions

This release extends the audit bundle so that replay fidelity covers input trust as well as verification logic.

New replay fields include:

- `transport_metadata`
- `revocation_status`
- `replay_contract`

## Replay contract

The replay contract now states whether:

- transport verification succeeded
- revocation freshness was evaluated
- deterministic inputs were present

## Why this matters

A replay artifact is more credible when it can show not only what the verifier did, but also whether the verifier had inputs that met the profile’s expectations.
