# Architecture

## Core idea

The verifier is no longer just a CAWG/C2PA request evaluator with TRQP-backed lookups. In `v0.12.0`, it becomes a **profile-governed policy execution engine**.

## Main components

- `cli.py` — request entrypoint and export workflow
- `verifier.py` — trust decision orchestration
- `profile.py` — profile loading, schema validation, and overlay composition
- `mock_service.py` — TRQP policy simulation
- `snapshot.py` — signed offline snapshot validation
- `audit.py` — deterministic audit bundle construction
- `replay.py` — re-execution against embedded profile and pinned feeds

## Execution flow

1. Load a request from JSON or fixture.
2. Resolve a verification profile from a built-in profile or supplied JSON path.
3. Apply zero or more assurance overlays.
4. Enforce the resulting control set during verification.
5. Emit a verification result carrying `policy_evidence.verification_profile`.
6. Optionally export an audit bundle containing `replay_inputs.profile`.

## Control domains

The profile model currently governs:

- authority trust posture
- freshness requirements
- revocation mode
- degraded-condition failure semantics
- evidence requirements
- replay determinism requirements

## Why this matters

This architecture makes verification behavior inspectable and testable. A consumer can now distinguish between:

- a result that was allowed to defer on policy outage
- a result that was required to reject on policy outage
- a result that required attested evidence
- a result that must be replayable from pinned inputs
