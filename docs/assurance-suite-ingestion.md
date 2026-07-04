# Assurance Suite Ingestion

## Purpose

The v0.16.0 conformance pack gives external TRQP and CAWG verifier suites a stable machine-readable entry point into this repository.

The primary artifact is:

- `conformance/assurance-suite-manifest.json`

It describes the reference implementation identity, fixture packages, assurance level interpretation, replay contracts, and evidence surfaces that another implementation can consume without scraping README text.

## Artifact Contract

Each fixture entry declares:

- `fixture_id`
- `profile`
- `assurance_level`
- `verification_mode`
- `vector_class`
- `implementation_identity`
- `inputs`
- `replay_contract`
- `fixture_path`

The contract is intentionally narrow. It does not require an external suite to adopt this repository's Python runtime. It only requires the suite to understand the request, profile, pinned feeds, expected result, and replay expectations.

## Assurance Level Interpretation

| Level | Meaning in this repository |
|---|---|
| `AL1` | Basic runtime trust evidence exists. |
| `AL2` | Operational trust evidence includes replay and revocation posture. |
| `AL3` | Mediated operation includes gateway route evidence. |
| `AL4` | High-assurance operation fails closed on required descriptor, revocation, transport, and evidence controls. |

## Generation and Validation

Regenerate the manifest after fixture or profile changes:

```bash
python scripts/export_conformance_pack.py
```

Validate that the committed artifact is current:

```bash
python scripts/export_conformance_pack.py --check
```

## Governance Use

The ingestion manifest is the handoff point between repository-local evidence and third-party assurance. It binds authority, profile, expected result, replay input, and evidence obligations into one portable declaration.
