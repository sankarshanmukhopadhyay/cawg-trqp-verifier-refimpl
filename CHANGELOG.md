# Changelog

All notable changes to the CAWG–TRQP reference implementation are documented here.

## [v0.4.0] – 2026-03-20

### Added

#### HTTP TRQP Service (Issue #003)
- `src/cawg_trqp_refimpl/http_service.py`: Flask-based HTTP service
- `/trqp/authorization` and `/trqp/recognition` endpoints
- `/health` health check endpoint
- `scripts/start_http_service.py`: Service startup script with CLI options
- `tests/test_http_service.py`: HTTP endpoint tests

#### CAWG/C2PA Manifest Parser (Issue #001)
- `src/cawg_trqp_refimpl/manifest_parser.py`: Signal extraction from manifests
- `ManifestSignal` dataclass for actor, issuer, assertions, and provenance
- Support for simplified fixtures (primary) and C2PA structures (fallback)
- Fixture validation helper

#### Revocation Delta Handling (Issue #004)
- `RevocationDelta` class in `verifier.py`
- `apply_revocation_delta()` method on Verifier
- Policy epoch tracking and timestamp recording
- "revocation_check" verification mode
- Active revocation checking in verify() workflow

#### Expanded Conformance Test Suite (Issue #005)
- `tests/test_conformance_vectors.py`: 20+ organized test cases
  - `TestStandardProfile`: cache-first behavior
  - `TestEdgeProfile`: offline snapshot verification
  - `TestHighAssuranceProfile`: live-only verification
  - `TestRevocation`: delta handling and blocking
  - `TestNegativeCases`: integrity failures, missing resources
  - `TestContextMatching`: context-sensitive authorization

#### Documentation
- `docs/INTEGRATION_GUIDE.md`: Complete step-by-step integration workflow
- README.md (rewritten): Clearer overview, architecture, quick start
- Updated references to upstream specs (CAWG, TRQP v2.0)

### Changed

- **pyproject.toml**: Version bump to 0.4.0, added `flask>=2.3.0` dependency
- **Verifier**: Enhanced with `apply_revocation_delta()` for policy invalidation
- **Test suite**: Expanded from ~80 lines to 300+ lines with comprehensive coverage

### Removed

- `RELEASE_NOTES_v0.3.0.md` (consolidated into changelog)
- `docs/release-readiness.md` (info merged into README status section)
- `docs/release-assets.md` (this release is the asset)
- `docs/repo-tree.md` (replaced with README structure)

### Documentation

- Added explicit references to upstream specs:
  - CAWG Specifications: https://cawg.io/specs/
  - TRQP v2.0 Specification: https://trustoverip.github.io/tswg-trust-registry-protocol/

## [v0.3.1] – 2026-03-20

### Added

- Explicit release-readiness assessment
- v0.3.1 release notes

### Changed

- Tightened public-facing README
- Refreshed repository tree documentation

## [v0.3.0] – 2026-03-19

### Added

- Release-readiness documentation
- Simplified CAWG/C2PA fixture ingestion
- Revocation data source (revocations.json)
- GitHub Actions CI workflow
- Roadmap and issue-ready gap log
- Expected result fixtures
- Improved repository structure for public release

## [v0.2.0] – 2026-03-18

### Added

- Executable reference implementation skeleton
- Mock TRQP service with policy and recognition queries
- TTL cache and snapshot loader
- Command-line interface
- Unit tests and demo runner
- Three verification profiles: edge, standard, high_assurance

---

**Repository Origin:** Solution to CAWG spec author's question: _"How do I integrate and implement a trust registry that uses TRQP into a CAWG-based workflow?"_
