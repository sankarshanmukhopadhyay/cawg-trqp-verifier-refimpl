# Issue 001: Add Real CAWG/C2PA Parser

**Status:** partially closed in v0.16.0  
**Resolution:** parser adapter boundary added; binary backend remains future work

## Outcome

v0.16.0 adds `src/cawg_trqp_refimpl/manifest_adapters.py` and documents the stable signal contract in `docs/parser-adapter-contract.md`.

The repository now has:

- `JsonManifestAdapter` for current JSON fixtures and C2PA-style JSON envelopes
- `C2PABinaryManifestAdapter` as a reserved integration boundary
- deterministic unsupported-backend behavior when a binary parser is not installed

## Remaining Work

Actual binary C2PA extraction should be added only when parser dependency licensing, fixture redistribution rights, and deterministic validation behavior are clear.
