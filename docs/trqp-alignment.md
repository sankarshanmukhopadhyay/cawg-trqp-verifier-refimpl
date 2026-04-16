# TRQP Alignment Surface

## Purpose

This document shows how `v0.13.0` lines up with broader TRQP assurance and conformance work.

The objective is not to claim full external alignment. The objective is to provide a clean handoff surface.

## Alignment points introduced in v0.13.0

### 1. Transport controls are now machine-readable

The profile schema now expresses transport requirements directly.

This gives external conformance tooling a stable way to check whether an implementation:

- distinguishes local, HTTP, and gateway paths
- captures transport integrity expectations
- differentiates required vs best-effort feed availability

### 2. Revocation freshness is now testable

The verifier now surfaces revocation freshness status as evidence.

This supports conformance-style checks around:

- stale revocation material
- warn vs fail behavior
- delta/live channel expectations

### 3. Replay fidelity is richer

Audit bundles now include transport metadata, revocation status, and replay contract fields.

This creates a stronger basis for independent re-execution and cross-implementation comparison.

### 4. Fixture exchange is now structured

The `fixtures/profile-bound/standard-v1/` package is intended as a starter exchange format for broader interoperability work.

## Suggested mapping areas for external suites

| Surface | Evidence produced by this repo | Likely external use |
|---|---|---|
| Profile schema | executable controls | static conformance checks |
| Verification result | runtime decision output | behavioral test assertions |
| Policy evidence | transport and revocation posture | assurance review and audit trails |
| Replay inputs | request, profile, feeds, replay contract | reproducibility testing |
| Fixture package | canonical exchange artifact | cross-implementation interoperability |

## Next alignment steps

- add machine-readable fixture manifests for additional profiles
- define expected negative outcomes for transport and freshness failures
- align fixture naming and metadata with TRQP conformance suite conventions
- add compatibility notes for downstream assurance hubs and registry ecosystems
