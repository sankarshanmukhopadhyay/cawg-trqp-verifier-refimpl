---
layout: default
title: Assurance Evidence
---

# Assurance evidence contract

Repository-native GitHub Actions runs are the authoritative evidence source for portfolio assurance.

| Claim | Required control | Freshness expectation |
|---|---|---|
| Implementation validation | `.github/workflows/ci.yml` | A successful completed execution inside the governed evidence window |
| Publication integrity | `.github/workflows/pages.yml` | A successful completed execution inside the governed evidence window |
| Package publication | repository release/package evidence | Optional |

Evidence is attributable only to the control that actually exercised the claim.

Portfolio finding lineage: `PF-5D9AA2B3D63F`, `PF-D930ABA3415C` (issue #35).

## Retest rule

Produce successful native CI and Pages evidence and rerun the Portfolio Assurance Monitor. Close only when both fingerprints are recorded as resolved.
