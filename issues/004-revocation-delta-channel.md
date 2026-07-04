# Issue 004: Add Revocation Delta Channel

**Status:** closed in v0.16.0  
**Resolution:** revocation posture is profile-controlled and replay-evidenced

## Outcome

The verifier evaluates revocation freshness, delta/live expectations, stale behavior, and fail-open or fail-closed semantics through verification profiles. Runtime evidence is carried into verification results and replay bundles.

## Evidence

- `src/cawg_trqp_refimpl/verifier.py`
- `src/cawg_trqp_refimpl/mock_service.py`
- `profiles/standard.json`
- `profiles/high_assurance.json`
- `tests/test_transport_and_replay_fidelity.py`
- `conformance/risk-to-test-map.yaml`
