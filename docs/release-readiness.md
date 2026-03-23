# Release Readiness

## Ready now

| Area | Status | Notes |
|---|---|---|
| repository structure | ready | coherent public layout |
| executable package | ready | installable via editable mode |
| CI workflow | ready | pytest runs in GitHub Actions |
| demo flow | ready | CLI and demo script included |
| test coverage | partial | core flows covered including process-aware paths |
| conformance vectors | partial | starter set included |
| edge snapshot behavior | ready | signed snapshot validation enforced |
| process-aware verification | ready | process requirements and appraisal included |
| public documentation | ready | README, roadmap, changelog, issues included |

## Not yet release-complete for production use

| Gap | Why it matters |
|---|---|
| full Proof of Process verifier stack | needed for deep evidence verification beyond compact fixture modeling |
| production TRQP transport and authn | needed for service deployment realism |
| audit bundle export | needed for portable evidence packaging |
| throughput benchmarking | needed for edge and high-volume evaluation |
| richer conformance vectors | needed for interop and regression breadth |

## Release assessment

This repository is suitable for:
- GitHub publication as a process-aware reference implementation
- design review
- engineering discussion
- standards-adjacent experimentation

It is not yet suitable as a production verifier.
