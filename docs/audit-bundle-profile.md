# Audit Bundle Profile

## Purpose

The audit bundle captures the verification decision and the evidence needed to replay and examine that decision later.

## Current bundle scope

The bundle now covers more than the verification result. It also carries the conditions under which the verifier trusted its inputs.

Important replay fields include:

- `transport_metadata`
- `revocation_status`
- `replay_contract`
- the resolved verification profile
- pinned policy and revocation feed references where available

## Replay contract

The replay contract states whether:

- transport verification succeeded
- revocation freshness was evaluated
- deterministic inputs were present
- pinned feeds were required by the selected profile

## Why this matters

A replay artifact is more credible when it can show not only what the verifier did, but also whether the verifier had inputs that met the profile’s expectations.

## Relationship to fixture packages

The audit bundle is the evidentiary artifact produced by a verification run. The canonical fixture packages under `fixtures/profile-bound/` are the exchange artifacts used to compare behavior across implementations.

The two surfaces complement each other:

- the audit bundle explains a concrete run
- the fixture package defines a portable test contract
