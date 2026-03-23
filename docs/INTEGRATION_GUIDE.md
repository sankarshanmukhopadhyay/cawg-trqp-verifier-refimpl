# CAWG–TRQP Integration Guide

## Overview

This repository shows how TRQP functions as the governance decision plane in a CAWG/C2PA verification flow and how Proof of Process style evidence can be introduced as a separate input to decision synthesis.

The operational pattern is straightforward:

1. parse provenance-bearing content metadata
2. extract actor, issuer, action, and process signals
3. query trust policy state through TRQP
4. evaluate process evidence against policy requirements
5. synthesize a trust decision that varies by deployment profile

## Separation of concerns

| Component | Responsibility |
|---|---|
| CAWG/C2PA manifest | provenance packaging and assertions |
| Identity material | actor and issuer binding |
| TRQP | authorization and recognition decisions |
| Process evidence | proof-oriented process signal |
| Verifier | profile-aware trust synthesis |

## Step 1: Parse the manifest

### Simplified fixture path

```python
from cawg_trqp_refimpl.manifest_parser import CAWGManifestParser

signal = CAWGManifestParser.parse_file("examples/fixtures/cawg_manifest_minimal.json")
print(signal.parser_mode)  # fixture
print(signal.process_evidence is not None)  # True
```

### C2PA-style JSON path

```python
signal = CAWGManifestParser.parse_file("examples/fixtures/cawg_manifest_c2pa_pop.json")
print(signal.parser_mode)   # c2pa_json
print(signal.actor_id)      # did:web:publisher.example
print(signal.action)        # publish
print(signal.process_evidence["process_type"])  # human_assisted
```

## Step 2: Build a verification request

Use the fixture loader when you want a deterministic request object from either input shape.

```python
from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture

request = load_manifest_fixture(
    "examples/fixtures/cawg_manifest_c2pa_pop.json",
    authority_id="did:web:media-registry.example",
)
```

## Step 3: Choose a profile

| Profile | Trust source | Typical environment |
|---|---|---|
| `edge` | signed snapshot only | disconnected or constrained device |
| `standard` | cache first, live on miss | services and platforms |
| `high_assurance` | live lookup only | regulated or audit-heavy workflows |

## Step 4: Verify online

```python
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.verifier import Verifier

verifier = Verifier(
    service=MockTRQPService(
        "data/policies.json",
        "data/revocations.json",
    )
)

result = verifier.verify(request, profile="standard")
print(result.trust_outcome)
print(result.process_integrity)
```

## Step 5: Verify offline with a signed snapshot

```python
from cawg_trqp_refimpl.snapshot import SnapshotStore
from cawg_trqp_refimpl.verifier import Verifier

snapshot = SnapshotStore(
    "data/snapshot.json",
    "data/trust_anchors.json",
)
verifier = Verifier(snapshot=snapshot)
result = verifier.verify(request, profile="edge")
print(result.policy_freshness)   # snapshot_verified
print(result.process_integrity)  # verified_high
```

### Edge trust path

For edge verification, the verifier now enforces this order:

1. load snapshot
2. verify Ed25519 signature using trust anchors
3. enforce `expires_at`
4. evaluate authorization and recognition from snapshot data
5. evaluate supplied process evidence against snapshot-carried process requirements
6. return `trusted_cached`, `rejected`, or `deferred`

## Policy shape

Authorization entries can now carry process requirements:

```json
{
  "authorized": true,
  "policy_requirements": {
    "requires_process_proof": true,
    "min_process_integrity": 0.75,
    "allowed_process_types": ["human_assisted", "verified_editorial_pipeline"]
  }
}
```

## Outcome interpretation

| Field | Meaning |
|---|---|
| `trust_outcome` | trusted, trusted_cached, rejected, or deferred |
| `actor_authorization` | authorized, not_authorized, or unknown |
| `issuer_recognition` | recognized or unknown |
| `process_integrity` | verified_high, verified, insufficient, failed, missing_required_proof, not_evaluated |
| `policy_freshness` | current, snapshot_verified, missing_snapshot, expired_snapshot, etc. |
| `verification_mode` | cached_online, online_full, offline_snapshot, or revocation_check |

## Reference path

The process-evidence examples in this repo are intentionally compact. They point toward the Proof of Process repository as a deeper source for evidence format and appraisal ideas:

- https://github.com/LF-Decentralized-Trust-labs/proof-of-process
