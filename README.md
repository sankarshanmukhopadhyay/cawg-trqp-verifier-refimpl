# CAWG-TRQP Reference Implementation

**Version line:** v0.16.0 roadmap closure and assurance hardening  
**Status:** executable reference implementation with schema-backed profiles, signed feed descriptors, deterministic replay, fixture exchange, HTTP service hardening, and external assurance-suite ingestion

## Overview

This repository shows how TRQP can operate as the governance decision plane for CAWG/C2PA-style content verification.

The verifier does more than return an allow or deny result. It records what authority was queried, which issuer was recognized, what process evidence was evaluated, which revocation posture was used, whether feed descriptors were valid, and whether the decision can be replayed from pinned inputs.

That makes the repository useful as:

- a developer reference implementation
- a conformance fixture source
- an assurance evidence model
- an HTTP deployment pattern
- a replayable governance decision example

## What v0.16.0 Adds

- Restores full test and validation health across examples, feed descriptors, audit bundles, replay bundles, and fixture packages.
- Adds profile-level descriptor policy with `observe`, `warn`, and `fail` semantics by feed type.
- Adds an external assurance-suite manifest at `conformance/assurance-suite-manifest.json`.
- Adds a parser adapter contract for future binary CAWG/C2PA extraction while preserving JSON fixture compatibility.
- Adds structured HTTP audit events for verification and audit-bundle routes.
- Adds release checksum tooling and `release-assets/checksums-v0.16.0.json`.
- Refreshes snapshot, fixture, replay, and audit-bundle artifacts so repository evidence is deterministic again.

## Quick Start

```bash
git clone <this-repo>
cd cawg-trqp-refimpl
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-lock.txt
pip install -e .
```

Run a standard verification:

```bash
python -m cawg_trqp_refimpl.cli examples/verification_request.json --profile standard
```

Run high-assurance verification with signed feed descriptors:

```bash
python -m cawg_trqp_refimpl.cli examples/verification_request.json \
  --profile high_assurance \
  --policy-descriptor examples/feed_descriptors/policy-feed.signed.json \
  --revocation-descriptor examples/feed_descriptors/revocation-feed.signed.json
```

Start the HTTP service:

```bash
python scripts/start_http_service.py \
  --policy-path data/policies.json \
  --revocation-path data/revocations.json \
  --host 127.0.0.1 \
  --port 5000
```

## Validation

Run the release validation gate:

```bash
python scripts/validate_examples.py
python scripts/validate_feed_descriptors.py
python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
python scripts/validate_photography_contest_example.py
python scripts/export_conformance_pack.py --check
python scripts/generate_release_checksums.py --check
pytest -q
```

Expected result for v0.16.0:

```text
68 passed
```

## Profiles

| Profile | Purpose | Descriptor posture |
|---|---|---|
| `standard` | Normal online or cached verification | Observe descriptor evidence |
| `high_assurance` | Live verification with fail-closed evidence requirements | Fail on policy, revocation, and gateway-route descriptor defects |
| `edge` | Offline snapshot verification | Fail on snapshot descriptor policy when configured |

Profiles are schema-backed by `schemas/verification-profile.schema.json`.

## Key Artifacts

| Path | Purpose |
|---|---|
| `src/cawg_trqp_refimpl/` | Verifier, service, replay, profile, descriptor, and parser code |
| `profiles/` | Built-in verification profiles and overlays |
| `schemas/` | JSON schemas for requests, results, profiles, receipts, descriptors, and audit bundles |
| `fixtures/profile-bound/` | Canonical fixture packages for external implementation comparison |
| `conformance/compatibility-matrix.json` | Machine-readable compatibility declaration |
| `conformance/assurance-suite-manifest.json` | External assurance-suite ingestion manifest |
| `examples/reproducibility_bundle_standard.json` | Canonical replay bundle |
| `examples/photography_contest/` | End-to-end contest verification walkthrough |
| `release-assets/checksums-v0.16.0.json` | Release asset checksum manifest |

## Documentation Map

- `docs/architecture.md`
- `docs/INTEGRATION_GUIDE.md`
- `docs/verifier-profiles.md`
- `docs/descriptor-policy.md`
- `docs/feed-descriptor-profile.md`
- `docs/reproducibility-guide.md`
- `docs/assurance-suite-ingestion.md`
- `docs/parser-adapter-contract.md`
- `docs/operational-hardening.md`
- `docs/how-trqp-enables-assurance.md`
- `docs/decision-receipt-specification.md`
- `docs/workflows/photography-contest-verification.md`

## Governance Model

The repository treats trust as executable governance:

- **Authority:** profile and policy feeds determine who can authorize or recognize.
- **Delegation:** gateway-mediated flows preserve route evidence and authority scope.
- **Enforcement:** revocation, descriptor policy, transport constraints, and process requirements affect outcomes.
- **Evidence:** decision results, decision receipts, audit bundles, replay bundles, and conformance manifests preserve auditability.
- **Revocation:** delta, live, and snapshot revocation postures are profile-controlled.
- **Replay:** pinned feeds and trusted replay roots make reliance decisions reproducible.

## Release Assets

Generate the external conformance manifest:

```bash
python scripts/export_conformance_pack.py
```

Generate release checksums:

```bash
python scripts/generate_release_checksums.py
```

The v0.16.0 release notes are in `RELEASE_NOTES_v0.16.0.md`.
