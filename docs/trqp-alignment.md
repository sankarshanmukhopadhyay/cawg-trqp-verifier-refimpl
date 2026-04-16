# TRQP Alignment Surface

## Purpose

This document shows how the current repository state lines up with broader TRQP assurance and conformance work.

The objective is not to claim full external alignment. The objective is to provide a clean handoff surface that another suite or implementation can consume.

## Current alignment points

### 1. Transport controls are machine-readable

The profile schema expresses transport requirements directly.

This gives external conformance tooling a stable way to check whether an implementation:

- distinguishes local, HTTP, and gateway paths
- captures transport integrity expectations
- differentiates required versus best-effort feed availability

### 2. Revocation freshness is testable

The verifier surfaces revocation freshness status as evidence.

This supports conformance-style checks around:

- stale revocation material
- warn versus fail behavior
- delta or live channel expectations

### 3. Replay fidelity is richer

Audit bundles include transport metadata, revocation status, and replay contract fields.

This creates a stronger basis for independent re-execution and cross-implementation comparison.

### 4. Fixture exchange is structured

The repository now publishes canonical profile-bound packages for standard, high-assurance, gateway-mediated, and multi-authority cases.

### 5. Compatibility coverage is machine-readable

`conformance/compatibility-matrix.json` gives downstream tooling a compact statement of what the repository currently covers and where the evidence for that claim lives.

## Suggested mapping areas for external suites

| Surface | Evidence produced by this repo | Likely external use |
|---|---|---|
| Profile schema | executable controls | static conformance checks |
| Verification result | runtime decision output | behavioral test assertions |
| Policy evidence | transport and revocation posture | assurance review and audit trails |
| Replay inputs | request, profile, feeds, replay contract | reproducibility testing |
| Fixture packages | canonical exchange artifacts | cross-implementation interoperability |
| Compatibility matrix | machine-readable coverage statement | assurance hub ingestion and program tracking |

## Next alignment steps

- align fixture metadata with broader TRQP conformance naming conventions
- let downstream assurance hubs ingest the compatibility matrix directly
- add richer freshness reason codes and stronger transport attestation semantics
- add compatibility statements for independent implementations that replay these packages successfully
