---
layout: default
title: "Contributing"
description: "The change workflow, pull request checklist, and evidence expectations."
parent: "Governance & Policy"
nav_order: 3
---
# Contributing

This repository is an executable reference implementation. Contributions should preserve the core adoption contract: examples must remain runnable, fixture packages must remain deterministic, and every governance decision must leave inspectable evidence.

## Change Workflow

1. Open or reference an issue before changing schemas, profiles, fixtures, or conformance artifacts.
2. Keep behavioral changes scoped to one concern: parser behavior, profile policy, feed descriptor validation, replay determinism, HTTP transport, or documentation.
3. Update generated evidence when source artifacts change.
4. Add or update tests for any change that alters verification outcomes, reason codes, descriptor policy, replay behavior, or audit-bundle shape.
5. Run the release validation gate before opening a pull request.

## Pull Request Checklist

- [ ] The change preserves backward compatibility or clearly documents the break.
- [ ] Relevant examples, fixtures, schemas, and docs are updated together.
- [ ] `python scripts/validate_examples.py` passes.
- [ ] `python scripts/validate_feed_descriptors.py` passes.
- [ ] `python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json` passes.
- [ ] `python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .` passes.
- [ ] `python scripts/validate_photography_contest_example.py` passes.
- [ ] `python scripts/export_conformance_pack.py --check` passes.
- [ ] `python scripts/generate_release_checksums.py --check` passes.
- [ ] `pytest -q` passes.

## Evidence Expectations

Verification changes should explain what authority was queried, what scope was enforced, what revocation posture applied, and what evidence allows the result to be audited or replayed.

Schema and fixture changes should include compatibility notes for downstream conformance consumers.
