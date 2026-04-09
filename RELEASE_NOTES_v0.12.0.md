# v0.12.0 — Executable Verification Profiles and Assurance Overlays

## Overview

This release turns verification profiles into machine-readable governance artifacts.

The verifier now resolves a profile, applies optional overlays, enforces the resulting controls at runtime, and carries the resolved profile into exported evidence and replay workflows.

## Highlights

- executable verification profile schema
- built-in `edge`, `standard`, and `high_assurance` profiles
- assurance overlays for stricter freshness and evidence postures
- fail-open / fail-closed behavior driven by profile controls
- audit bundle export with embedded resolved profile object
- replay using profile-bound governance semantics rather than local assumptions

## Why this matters

Verification output is no longer only a trust decision. It is now also evidence of:

- which authority posture applied
- whether degraded policy conditions were allowed to defer or required rejection
- whether attested evidence was mandatory
- whether deterministic replay guarantees were expected

## Validation performed

- `pytest -q`
- `python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json`
- `python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json`
- `python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json`
