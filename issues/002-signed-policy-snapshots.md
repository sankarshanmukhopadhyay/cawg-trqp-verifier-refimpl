# Issue 002: Add Signed Policy Snapshots

**Status:** closed in v0.16.0  
**Resolution:** signed snapshot verification and descriptor freshness restored

## Outcome

The repository verifies offline snapshot signatures using configured trust anchors. v0.16.0 refreshes `data/snapshot.json`, re-signs it, and updates `examples/feed_descriptors/snapshot-feed.signed.json` so descriptor digest validation passes.

## Evidence

- `src/cawg_trqp_refimpl/snapshot.py`
- `scripts/sign_snapshot.py`
- `data/snapshot.json`
- `examples/feed_descriptors/snapshot-feed.signed.json`
- `tests/test_snapshot.py`
