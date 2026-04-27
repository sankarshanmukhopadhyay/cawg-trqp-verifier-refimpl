# Photography Contest Runnable Example

This directory contains a runnable demo aligned with `docs/workflows/photography-contest-verification.md`. It models a user-submitted heritage photography contest submission and shows how the verifier produces evidence that can be replayed during review or appeal.

## Files

- `submission.json` — the participant submission converted into a verifier request.
- `contest_policy_feed.json` — the contest rule and authorization feed.
- `contest_revocation_feed.json` — the revocation/disqualification feed.
- `policy-feed.signed.json` — signed descriptor for the contest policy feed.
- `revocation-feed.signed.json` — signed descriptor for the revocation feed.
- `trust_anchors.json` — public trust anchor for the demo feed authority.
- `decision_receipt.json` — participant/reviewer-facing decision receipt.
- `replay_bundle.json` — audit bundle that can be replayed with the standard replay script.

## Run

```bash
python scripts/validate_photography_contest_example.py
python scripts/replay_audit_bundle.py examples/photography_contest/replay_bundle.json
```

Expected result: replay reports `matches: true` with no differences.
