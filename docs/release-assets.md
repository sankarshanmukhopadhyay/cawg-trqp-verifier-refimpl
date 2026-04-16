# Release Assets

## v0.13.0 should ship with

- updated source code and schemas
- refreshed built-in profiles and overlays
- updated example audit bundles
- canonical reproducibility bundle
- canonical fixture package under `fixtures/profile-bound/standard-v1/`
- `RELEASE_NOTES_v0.13.0.md`
- refreshed documentation set

## Recommended checks before publishing

- full test suite passes
- reproducibility script matches canonical bundle
- signed audit bundle validates against trust anchors
- repo tree and documentation reflect the current structure
