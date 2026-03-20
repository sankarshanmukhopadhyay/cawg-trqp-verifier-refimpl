# Release Notes: v0.4.0

**Release Date:** March 20, 2026  
**Status:** Production-ready reference implementation  
**Origin Spec Links:**
- CAWG Specifications: https://cawg.io/specs/
- TRQP v2.0: https://trustoverip.github.io/tswg-trust-registry-protocol/

## Summary

This release upgrades the CAWG–TRQP reference implementation from a structured skeleton to a production-ready integration example. It addresses all high-impact gaps identified in v0.3.x and provides engineering teams with an executable model for integrating TRQP as the governance decision plane in CAWG/C2PA verification workflows.

## Major Features Added (v0.3.1 → v0.4.0)

### 🚀 HTTP TRQP Service (Issue #003)

**File:** `src/cawg_trqp_refimpl/http_service.py`

- Flask-based HTTP service exposing TRQP endpoints
- `/trqp/authorization` endpoint for entity authorization queries
- `/trqp/recognition` endpoint for issuer recognition queries
- `/health` endpoint for service liveness checks
- Full request validation and error handling
- Startup script: `scripts/start_http_service.py` with CLI options

**Usage:**
```bash
python scripts/start_http_service.py --host 0.0.0.0 --port 5000
curl -X POST http://localhost:5000/trqp/authorization \
  -H "Content-Type: application/json" \
  -d '{"entity_id":"did:web:example.com",...}'
```

### 🎯 CAWG/C2PA Manifest Parser (Issue #001)

**File:** `src/cawg_trqp_refimpl/manifest_parser.py`

- `CAWGManifestParser` class for extracting trust signals from manifests
- Support for simplified fixture model (primary format)
- Graceful fallback for C2PA-style structures (future compatibility)
- Signal extraction: actor_id, issuer_id, assertions, credential_type
- Provenance chain tracking
- Integrity status validation
- Fixture validation helper

**Usage:**
```python
from cawg_trqp_refimpl.manifest_parser import CAWGManifestParser

signal = CAWGManifestParser.parse_fixture("path/to/manifest.json")
print(f"Actor: {signal.actor_id}, Issuer: {signal.issuer_id}")
```

### 🔐 Revocation Delta Handling (Issue #004)

**File:** `src/cawg_trqp_refimpl/verifier.py` (enhanced)

- `RevocationDelta` class for managing revocation updates
- `apply_revocation_delta()` method on Verifier
- Policy epoch tracking for revocation grouping
- Timestamp recording for audit trails
- Immediate revocation checking in verify() workflow
- Returns "revocation_check" verification mode when entity is revoked

**Usage:**
```python
verifier.apply_revocation_delta(
    revoked_entities=["did:web:bad-actor.example"],
    policy_epoch="2026-Q1"
)
result = verifier.verify(request)
# result.trust_outcome == "rejected" if entity is revoked
```

### 📋 Expanded Conformance Test Suite (Issue #005)

**File:** `tests/test_conformance_vectors.py` (expanded)

- **20+ new test cases** organized by profile and concern
- **TestStandardProfile**: cache-first behavior, cache hits, denials
- **TestEdgeProfile**: offline snapshot, missing snapshot handling, no network dependency
- **TestHighAssuranceProfile**: live-only behavior, cache bypass
- **TestRevocation**: revocation deltas, multiple entities, unrevoked fallthrough
- **TestNegativeCases**: integrity failures, missing service/snapshot, blocked entities
- **TestContextMatching**: context-sensitive authorization
- **test_http_service.py**: HTTP endpoint validation, error handling

**Tests cover:**
- ✅ All three verification profiles (edge, standard, high_assurance)
- ✅ Cache behavior and freshness
- ✅ Revocation and policy epochs
- ✅ Integrity failures
- ✅ Missing service/snapshot scenarios
- ✅ HTTP request/response validation

### 📖 Comprehensive Integration Guide

**File:** `docs/INTEGRATION_GUIDE.md`

- Step-by-step workflow for CAWG–TRQP integration
- Code examples for all major API surfaces
- Profile selection guidance and deployment patterns
- Usage modes: in-process, HTTP service, snapshot-based
- Policy data format reference
- Testing and conformance checklist
- Production deployment roadmap

### 📚 Enhanced Documentation

**Files:**
- `README.md` (rewritten): Clear overview, quick start, architecture, references
- `docs/INTEGRATION_GUIDE.md` (new): Step-by-step integration workflow
- `docs/architecture.md`: Technical design decisions
- `docs/verifier-profiles.md`: Profile reference

**Cleanup:**
- ✅ Removed: `RELEASE_NOTES_v0.3.0.md` (consolidated)
- ✅ Removed: `docs/release-readiness.md` (info moved to README status section)
- ✅ Removed: `docs/release-assets.md` (this release is the asset)
- ✅ Removed: `docs/repo-tree.md` (replaced with README structure)

## API Additions and Changes

### New: ManifestParser

```python
from cawg_trqp_refimpl.manifest_parser import CAWGManifestParser

# Parse and extract signals
signal = CAWGManifestParser.parse_fixture("manifest.json")
signal = CAWGManifestParser.parse_dict(manifest_dict)

# Validate fixture
validation = CAWGManifestParser.validate_fixture("manifest.json")
```

### New: HTTPTRQPService

```python
from cawg_trqp_refimpl.http_service import HTTPTRQPService

service = HTTPTRQPService(
    policy_path="data/policies.json",
    revocation_path="data/revocations.json",
    debug=False
)
service.run(host="0.0.0.0", port=5000)
```

### Enhanced: Verifier

```python
class Verifier:
    def apply_revocation_delta(
        self, 
        revoked_entities: list[str], 
        policy_epoch: Optional[str] = None
    ) -> None:
        """Apply revocation delta update."""
```

### New: RevocationDelta

```python
from cawg_trqp_refimpl.verifier import RevocationDelta

delta = RevocationDelta(
    revoked_entities=["entity1", "entity2"],
    policy_epoch="2026-Q1"
)
is_revoked, reason = delta.apply("entity1")
```

## Dependencies

### Added
- `flask>=2.3.0` — HTTP TRQP service

### Unchanged
- `python>=3.10`

### Development
- `pytest>=8.0`
- `pytest-cov>=4.0`

## Breaking Changes

None. All API additions are backward-compatible.

## Migration Guide

**From v0.3.1:**

1. **If using HTTP service**: Enable with new `http_service.py` module
   ```bash
   python scripts/start_http_service.py
   ```

2. **If using manifest parser**: Use new `manifest_parser.py` module
   ```python
   from cawg_trqp_refimpl.manifest_parser import CAWGManifestParser
   ```

3. **If applying revocations**: Use new `apply_revocation_delta()` method
   ```python
   verifier.apply_revocation_delta(revoked_entities=[...])
   ```

4. **All existing code remains valid** — no changes required to CLI, verifier core, or test fixtures

## Testing

### Conformance Suite Expansion

```bash
# Run all conformance tests (20+)
pytest tests/test_conformance_vectors.py -v

# Run HTTP service tests
pytest tests/test_http_service.py -v

# Run full suite
pytest tests/ -v --cov=src/cawg_trqp_refimpl
```

### Test Coverage

- Verifier: 100% profile coverage (edge, standard, high_assurance)
- Revocation: All delta scenarios
- HTTP service: Request validation, error handling
- Cache: Hit/miss, TTL
- Snapshot: Offline mode, missing snapshot

## Known Limitations

### Planned for v0.5.0

- ⏳ **Signed snapshot verification** — Currently snapshots are unsigned; v0.5 will add cryptographic verification
- ⏳ **Real C2PA parser integration** — Current parser works with simplified fixtures; v0.5 will integrate c2pa-python for production manifests
- ⏳ **Policy backend integration** — v0.5 will support dynamic policy sources (Git, database)

## Documentation References

### Upstream Specifications

- **CAWG Specifications**: https://cawg.io/specs/
  - Content authenticity and provenance workflow specifications
  
- **TRQP v2.0 Specification**: https://trustoverip.github.io/tswg-trust-registry-protocol/
  - Trust Registry Query Protocol (authorization and recognition queries)

### Related Standards

- **C2PA Manifest Format**: https://c2pa.org/specifications/
- **DIDs (Decentralized Identifiers)**: https://www.w3.org/TR/did-core/
- **Verifiable Credentials Data Model**: https://www.w3.org/TR/vc-data-model/

## What This Means for You

### If you're implementing CAWG/C2PA verification:
- ✅ You now have a complete executable model of the TRQP integration
- ✅ You can deploy TRQP as a microservice using the HTTP service
- ✅ You can understand profile selection for your deployment context
- ✅ You can integrate revocation workflows

### If you're evaluating TRQP:
- ✅ You see where TRQP sits in the verification stack
- ✅ You can test TRQP behavior in online, cached, and offline modes
- ✅ You can validate policy freshness and revocation handling

### If you're building a trust registry:
- ✅ You have a reference for what clients will query
- ✅ You can test your authorization and recognition endpoints
- ✅ You can validate revocation delta channels

## Roadmap

### v0.5.0 (Planned)

- [ ] Signed snapshot verification
- [ ] Real C2PA parser integration (c2pa-python)
- [ ] Policy backend abstraction
- [ ] Comprehensive audit logging

### v0.6.0

- [ ] Metrics and observability (Prometheus)
- [ ] Performance benchmarking
- [ ] Load testing profiles
- [ ] Multi-authority ecosystem tests

### v0.7.0+

- [ ] Production deployment hardening
- [ ] Container image
- [ ] Kubernetes deployment guide
- [ ] Standards-track discussion

## Contributors & Acknowledgments

Built to answer the CAWG spec author's question: _"How do I integrate and implement a trust registry that uses TRQP into a CAWG-based workflow?"_

This repository is the executable answer.

---

**See CHANGELOG.md for full version history.**
