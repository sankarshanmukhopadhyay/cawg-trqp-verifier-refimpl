## Summary

<!-- What does this change do, and why? -->

## Scope

<!-- One concern: parser behavior, profile policy, feed descriptor validation,
     replay determinism, HTTP transport, documentation, or repository hygiene. -->

## Evidence

- [ ] Relevant examples, fixtures, schemas, and docs are updated together.
- [ ] `python scripts/validate_examples.py` passes.
- [ ] `python scripts/validate_feed_descriptors.py` passes.
- [ ] `python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json` passes.
- [ ] `python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .` passes.
- [ ] `python scripts/validate_photography_contest_example.py` passes.
- [ ] `python scripts/export_conformance_pack.py --check` passes.
- [ ] `python scripts/generate_release_checksums.py --check` passes.
- [ ] `pytest -q` passes.

Paste the actual output of the commands you ran (pass/fail counts), not just a checkmark.

## Compatibility

<!-- Does this preserve backward compatibility? If not, what breaks, and for whom
     (downstream conformance consumers, existing profiles, existing fixtures)? -->

## Authority and governance

<!-- Does this change something the repository owns (verifier behavior,
     profiles/fixtures, evidence formats) or touch something it explicitly
     does not own (TRQP spec, CAWG/C2PA standards)? See GOVERNANCE.md. -->

## AI assistance

- [ ] No material AI assistance was used.
- [ ] Material AI assistance was used and is described below, including human validation performed.

Details: 
