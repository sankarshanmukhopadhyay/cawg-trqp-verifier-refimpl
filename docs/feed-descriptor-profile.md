# Feed Descriptor Profile

**Release:** v0.14.0  
**Purpose:** make policy, revocation, snapshot, and gateway feed inputs independently attestable before a verifier relies on them.

## Why this exists

TRQP verification depends on external control-plane inputs. A verifier can record that it used a policy feed, but that is not enough for runtime assurance. The feed itself must carry authority, digest, freshness, route, and signature evidence so an auditor can answer four operational questions:

1. Which authority published the feed?
2. Was the feed body the feed the authority attested?
3. Was the feed fresh enough for the selected profile?
4. Was a gateway-mediated route attested rather than merely implied?

## Descriptor surfaces

| Surface | Example | Assurance question |
| --- | --- | --- |
| Policy feed | `examples/feed_descriptors/policy-feed.signed.json` | Which policy state authorized the actor? |
| Revocation feed | `examples/feed_descriptors/revocation-feed.signed.json` | Was withdrawal state available and current? |
| Snapshot feed | `examples/feed_descriptors/snapshot-feed.signed.json` | Can offline verification prove pinned inputs? |
| Gateway route feed | `examples/feed_descriptors/gateway-route-feed.signed.json` | Was mediation route evidence produced? |

## Runtime evidence model

The verifier exports descriptor validation reports under:

```json
{
  "policy_evidence": {
    "feed_descriptors": {
      "policy": {"reason_code": "fresh"},
      "revocation": {"reason_code": "fresh"}
    }
  }
}
```

The same object is also copied into audit bundle replay inputs. This is intentional: replay should not merely replay the request and result; it should also preserve the feed authority and integrity posture available at decision time.

## Reason codes

The profile normalizes freshness and descriptor failures into stable reason codes:

- `fresh`
- `stale_but_warned`
- `stale_rejected`
- `missing_feed_descriptor`
- `descriptor_signature_invalid`
- `descriptor_digest_mismatch`
- `authority_not_recognized`
- `route_unattested`
- `revocation_channel_degraded`

## Validation

```bash
python scripts/validate_feed_descriptors.py
python scripts/validate_examples.py
pytest -q
```

## Adoption guidance

For production integration, treat descriptors as the minimum deployable contract for any feed that influences authorization or revocation. Systems can begin in observation mode by validating descriptors and logging reason codes, then move to fail-closed enforcement for high-assurance profiles once operational baselines are stable.
