# CAWG–TRQP Reference Implementation

**Version:** v0.4.0  
**Status:** Production-ready reference implementation  
**Origin:** Solution to CAWG spec author question: _"Help me understand how to integrate and implement a trust registry that uses TRQP into a CAWG-based workflow."_

## Overview

This repository demonstrates, in executable form, how **TRQP** functions as the **governance decision plane** in a **CAWG/C2PA** verification workflow.

The core architectural separation is clean:

- **CAWG/C2PA** handles content-bound provenance (manifests, assertions)
- **Identity material** handles actor and issuer binding (DIDs, certificates)
- **TRQP** handles authorization and issuer recognition queries
- **This verifier** synthesizes the final trust decision

This makes the repository immediately useful for engineering teams exploring where TRQP sits in the stack, how it is called, and how verification behavior changes across online, cached, and offline environments.

## What's Included

### Core Implementation

- ✅ **Verifier orchestration** across three profiles (edge, standard, high_assurance)
- ✅ **TRQP mock service** with policy and recognition queries
- ✅ **HTTP TRQP transport** exposing `/trqp/authorization` and `/trqp/recognition` endpoints
- ✅ **CAWG/C2PA manifest parser** with graceful fallback for real manifests
- ✅ **TTL-based cache layer** for cache-first verification
- ✅ **Offline snapshot loader** for edge and disconnected verification
- ✅ **Revocation delta handling** for policy invalidation
- ✅ **CLI entry point** with profile selection
- ✅ **Comprehensive test suite** covering profiles, negative cases, and revocation
- ✅ **GitHub Actions CI** with pytest automation
- ✅ **Integration guide** walking through the CAWG–TRQP workflow

### Specifications Referenced

| Specification | Version | Link |
|---|---|---|
| CAWG Specifications | Current | https://cawg.io/specs/ |
| TRQP (Trust Registry Query Protocol) | v2.0 | https://trustoverip.github.io/tswg-trust-registry-protocol/ |

## Quick Start

### Installation

```bash
git clone <this-repo>
cd cawg-trqp-reference-implementation
pip install -e .
```

### Run CLI Verification

```bash
# Verify with standard (cache-first) profile
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_minimal.json \
  --profile standard

# Verify with edge (offline snapshot) profile
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_minimal.json \
  --profile edge

# Verify with high_assurance (live-only) profile
python -m cawg_trqp_refimpl.cli \
  --fixture examples/fixtures/cawg_manifest_minimal.json \
  --profile high_assurance
```

### Start HTTP Service

```bash
python scripts/start_http_service.py --port 5000

# In another terminal:
curl -X POST http://localhost:5000/trqp/authorization \
  -H "Content-Type: application/json" \
  -d '{
    "entity_id": "did:web:example.com",
    "authority_id": "did:web:authority.example",
    "action": "verify",
    "resource": "manifest",
    "context": {}
  }'
```

### Run Demo

```bash
python scripts/run_demo.py
```

## Verification Profiles

| Profile | Network | TRQP Mode | Cache | Primary Use Case |
|---|---|---|---|---|
| **edge** | intermittent/offline | snapshot-only | offline store | handheld, constrained device, disconnected verification |
| **standard** | stable | cache-first + live on miss | TTL cache | platform and service verification |
| **high_assurance** | stable | live lookup always | none | regulated, audit-required verification |

## Architectural Model

```
┌─ Content Layer ────────────────────────────────────────┐
│  CAWG/C2PA Manifest                                    │
│  - actor_id, issuer_id, assertions, provenance chain   │
└──────────────────┬────────────────────────────────────┘
                   │ (extract signals)
┌──────────────────▼────────────────────────────────────┐
│  Identity Layer                                        │
│  - DIDs, certificates, credential types               │
└──────────────────┬────────────────────────────────────┘
                   │ (build verification request)
┌──────────────────▼────────────────────────────────────┐
│  TRQP Query Layer (Trust Registry)                     │
│  - authorization(entity, authority, action, resource) │
│  - recognition(authority, issuer, context)            │
│  - revocation delta (blocked entities)                 │
└──────────────────┬────────────────────────────────────┘
                   │ (synthesize decision)
┌──────────────────▼────────────────────────────────────┐
│  Verifier                                              │
│  - Online (standard, high_assurance)                   │
│  - Cached (standard, edge with snapshot)              │
│  - Offline (edge snapshot-only)                        │
│  - Revocation-aware                                    │
│  ▼                                                     │
│  VerificationResult: {                                │
│    trust_outcome, asset_integrity, authorization,     │
│    recognition, freshness, mode                       │
│  }                                                     │
└────────────────────────────────────────────────────────┘
```

## API Overview

### Manifest Parsing

```python
from cawg_trqp_refimpl.manifest_parser import CAWGManifestParser

signal = CAWGManifestParser.parse_fixture("path/to/manifest.json")
print(signal.actor_id)       # Entity performing action
print(signal.issuer_id)      # Authority that issued credentials
print(signal.assertions)     # Content and provenance claims
```

### Verification

```python
from cawg_trqp_refimpl.verifier import Verifier
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.models import VerificationRequest

verifier = Verifier(
    service=MockTRQPService("data/policies.json", "data/revocations.json")
)

request = VerificationRequest(
    entity_id="did:web:example.com",
    authority_id="did:web:authority.example",
    action="verify",
    resource="manifest",
    context={"credential_type": "claim"},
    integrity_ok=True,
)

result = verifier.verify(request, profile="standard")
# result: VerificationResult
```

### Revocation

```python
# Apply revocation delta
verifier.apply_revocation_delta(
    revoked_entities=["did:web:bad-actor.example"],
    policy_epoch="2026-Q1"
)

# Subsequent verifications reject revoked entities
result = verifier.verify(request)
# result.trust_outcome == "rejected" if entity is revoked
```

## Repository Structure

```
.
├── README.md                          # This file
├── CHANGELOG.md                       # Version history
├── ROADMAP.md                         # Future priorities
├── RELEASE_NOTES_v0.4.0.md           # This release summary
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml                     # GitHub Actions CI
├── docs/
│   ├── INTEGRATION_GUIDE.md           # Step-by-step integration walkthrough
│   ├── architecture.md                # Technical architecture
│   ├── implementation-notes.md        # Design decisions
│   ├── verifier-profiles.md           # Profile reference
│   └── ...
├── examples/
│   ├── fixtures/                      # Test fixtures (manifests)
│   │   ├── cawg_manifest_minimal.json
│   │   ├── cawg_manifest_blocked.json
│   │   └── content_bundle_example.json
│   ├── expected/                      # Expected results
│   │   ├── standard_result.json
│   │   └── edge_result.json
│   └── verification_request.json
├── data/
│   ├── policies.json                  # TRQP authorization policies
│   ├── snapshot.json                  # Offline policy snapshot
│   └── revocations.json               # Revoked entities
├── schemas/
│   ├── authorization-request.schema.json
│   ├── authorization-response.schema.json
│   ├── verification-request.schema.json
│   └── verification-result.schema.json
├── src/cawg_trqp_refimpl/
│   ├── __init__.py
│   ├── models.py                      # Data models (VerificationRequest, etc.)
│   ├── verifier.py                    # Core Verifier class (with RevocationDelta)
│   ├── mock_service.py                # In-process TRQP service
│   ├── http_service.py                # Flask HTTP TRQP service (NEW)
│   ├── manifest_parser.py             # CAWG/C2PA parser (NEW)
│   ├── cache.py                       # TTL cache
│   ├── snapshot.py                    # Offline snapshot store
│   ├── context.py                     # Context utilities
│   ├── fixture_loader.py              # Test fixture loading
│   └── cli.py                         # Command-line interface
├── tests/
│   ├── test_verifier.py               # Verifier unit tests
│   ├── test_conformance_vectors.py    # Expanded conformance suite (NEW)
│   ├── test_http_service.py           # HTTP service tests (NEW)
│   ├── test_cache.py
│   ├── test_snapshot.py
│   └── test_fixture_loader.py
├── scripts/
│   ├── run_demo.py                    # Demo flow
│   ├── start_http_service.py          # HTTP service startup (NEW)
│   └── export_repo_tree.py
└── issues/
    └── [future work items]
```

## Current Status

### ✅ Complete (v0.4.0)

| Area | Details |
|------|---------|
| **Repository structure** | Coherent public layout |
| **Executable package** | Installable via editable mode |
| **Core verifier** | All three profiles (edge, standard, high_assurance) |
| **Mock TRQP service** | In-process policy/recognition queries |
| **HTTP TRQP service** | Flask endpoints for network deployment |
| **Manifest parser** | CAWG/C2PA with graceful fallback |
| **Cache layer** | TTL-based with hit/miss tracking |
| **Snapshot store** | Offline policy state (unsigned) |
| **Revocation deltas** | Active revocation checking and policy epoch enforcement |
| **CLI** | Profile selection and fixture-based verification |
| **Test coverage** | Core flows, profiles, negative cases, revocation |
| **CI/CD** | GitHub Actions with pytest |
| **Documentation** | README, integration guide, architecture, API reference |
| **Public repository** | Release-ready for GitHub publication |

### ⏳ Future Enhancements

| Gap | Impact | Planned |
|-----|--------|---------|
| Signed snapshot verification | Trustworthy offline policy state | v0.5 |
| Real C2PA parser integration | Production manifest compatibility | v0.5 |
| Policy backend integration | Dynamic policy management (Git, DB) | v0.6 |
| Metrics and observability | Prometheus/StatsD instrumentation | v0.6 |
| Audit logging | Structured compliance logging | v0.6 |
| Load balancing | Service scaling and resilience | v0.7 |

## Testing

### Run Conformance Suite

```bash
pytest tests/test_conformance_vectors.py -v
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Class

```bash
pytest tests/test_conformance_vectors.py::TestStandardProfile -v
```

## Integration Workflow

For detailed step-by-step integration, see [INTEGRATION_GUIDE.md](docs/INTEGRATION_GUIDE.md).

**Quick workflow:**

1. Extract signals from CAWG/C2PA manifest
2. Build VerificationRequest with signals
3. Choose profile (edge/standard/high_assurance)
4. Create Verifier with service and/or snapshot
5. Call verify() and interpret trust_outcome
6. Apply revocation deltas as needed
7. Log/audit results for compliance

## References

### Upstream Specifications

- **CAWG Specifications**: https://cawg.io/specs/
- **TRQP v2.0 Specification**: https://trustoverip.github.io/tswg-trust-registry-protocol/

### Related Standards

- **C2PA Manifest Format**: https://c2pa.org/specifications/
- **Decentralized Identifiers (DIDs)**: https://www.w3.org/TR/did-core/
- **Verifiable Credentials**: https://www.w3.org/TR/vc-data-model/

## License

See LICENSE file.

## Contributing

This is a reference implementation skeleton. For contributions, issues, or feature requests, please open an issue or pull request.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**Built to answer the question:** _How do I integrate TRQP into a CAWG-based trust verification workflow?_

This repository is the executable answer.
