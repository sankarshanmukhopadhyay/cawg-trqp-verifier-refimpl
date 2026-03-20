# Release Readiness

## Ready now

| Area | Status | Notes |
|---|---|---|
| repository structure | ready | coherent public layout |
| executable package | ready | installable via editable mode |
| CI workflow | ready | pytest runs in GitHub Actions |
| demo flow | ready | CLI and demo script included |
| test coverage | partial | core flows covered |
| conformance vectors | partial | starter set included |
| edge snapshot behavior | partial | modeled without signature verification |
| public documentation | ready | README, roadmap, changelog, issues included |

## Not yet release-complete for production use

| Gap | Why it matters |
|---|---|
| real CAWG/C2PA parser | needed for parser-level interoperability |
| signed snapshot verification | needed for trustworthy offline policy state |
| HTTP TRQP transport | needed for service deployment realism |
| revocation delta handling | needed for realistic freshness invalidation |
| throughput benchmarking | needed for edge and high-volume evaluation |

## Release assessment

This repository is suitable for:
- GitHub publication as a reference implementation skeleton
- design review
- engineering discussion
- standards-adjacent experimentation

It is not yet suitable as a production verifier.
