# CAWG–TRQP Reference Implementation

Version: v0.3.1  
Status: Release-ready reference implementation skeleton

## Why this exists

This repository demonstrates, in executable form, how **TRQP** functions as the **governance decision plane** in a **CAWG/C2PA** verification workflow.

The core architectural split is simple:

- **CAWG/C2PA** handles content-bound provenance
- **identity material** handles actor and issuer binding
- **TRQP** handles authorization and recognition
- **the verifier** synthesizes the final trust decision

That makes this repository useful for engineering teams that want to explore where TRQP sits in the stack, how it is called, and how verification behavior changes across online, cached, and offline environments.

## What is included

- Python package structure
- mock TRQP policy service
- TTL-based cache layer
- snapshot loader for offline and edge verification
- simplified CAWG/C2PA-style fixture ingestion
- verifier orchestration logic
- CLI entry point
- tests and conformance fixtures
- GitHub Actions CI workflow
- roadmap, changelog, and issue-ready gap notes

## Verification profiles

| Profile | Network posture | TRQP mode | Primary use case |
|---|---|---|---|
| `edge` | intermittent / offline | snapshot | small node, handheld, constrained device |
| `standard` | stable | cache-first + live on miss | platform and service verification |
| `high_assurance` | stable | live lookup | regulated or high-assurance verification |

## Quick start

```bash
pip install -e .
python -m cawg_trqp_refimpl.cli --fixture examples/fixtures/cawg_manifest_minimal.json --profile standard
python scripts/run_demo.py
```

## Repository layout

```text
.
├── README.md
├── LICENSE
├── CHANGELOG.md
├── ROADMAP.md
├── RELEASE_NOTES_v0.3.1.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
├── issues/
├── examples/
├── data/
├── schemas/
├── src/
│   └── cawg_trqp_refimpl/
├── tests/
└── scripts/
```

## Current boundary

This repository uses a simplified CAWG/C2PA fixture model rather than a full parser for production manifests. That is deliberate. The immediate goal is to make the **position and behavior of TRQP** implementation-clear before introducing heavier parsing and transport dependencies.

## Near-term priorities

1. Add real CAWG/C2PA parsing.
2. Add signed policy snapshot verification.
3. Expose the mock TRQP service over HTTP.
4. Expand conformance vectors and failure-mode coverage.
5. Add throughput and cache-behavior benchmarking.
