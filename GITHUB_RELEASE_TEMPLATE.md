# GitHub Release Template

Reusable template for drafting a GitHub Release. Copy this into the release
description, fill in the placeholders, and delete this comment block.

The most recent actual release notes are always in `RELEASE_NOTES_v<version>.md`
at the repository root; the changelog entry in `CHANGELOG.md` under
`## v<version>` should match. This file is a *template*, not a record of any
specific past release.

## Title

`v<version> — <short theme, e.g. "Security Hardening" or "Verified Quickstart & CI Parity">`

## Summary

One or two sentences: what does this release change for someone consuming
the repository, not just for the maintainer?

## Highlights

- <capability or fix, in outcome terms, not implementation terms>
- <capability or fix>
- <capability or fix>

## Compatibility

State plainly whether this is backward compatible. If downstream conformance
consumers, existing profiles, or existing fixtures are affected, say exactly
what changes and what they need to do.

## Validation

Paste the actual command output (pass/fail counts), not just the commands:

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

## Release checklist

- [ ] `CHANGELOG.md` has a matching `## v<version>` entry.
- [ ] `RELEASE_NOTES_v<version>.md` exists at the repository root.
- [ ] `CITATION.cff` `version` and `date-released` are updated.
- [ ] `data/repository-metadata.yaml` `current_version` is updated.
- [ ] `release-assets/checksums-v<version>.json` generated via `python scripts/generate_release_checksums.py`.
- [ ] Validation gate above passes and output is pasted into this release.
