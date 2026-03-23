# CAWG–TRQP Integration Guide

## Overview

This repository shows how TRQP functions as the governance decision plane in a CAWG/C2PA verification flow.

The operational pattern is straightforward:

1. parse provenance-bearing content metadata
2. extract actor, issuer, and action signals
3. query trust policy state through TRQP
4. synthesize a trust decision that varies by deployment profile

## Separation of concerns

| Component | Responsibility |
|---|---|
| CAWG/C2PA manifest | provenance packaging and assertions |
| Identity material | actor and issuer binding |
| TRQP | authorization and recognition decisions |
| Verifier | profile-aware trust synthesis |

## Step 1: Parse the manifest

### Simplified fixture path

```python
from cawg_trqp_refimpl.manifest_parser import CAWGManifestParser

signal = CAWGManifestParser.parse_file("examples/fixtures/cawg_manifest_minimal.json")
print(signal.parser_mode)  # fixture
```

### C2PA-style JSON path

```python
signal = CAWGManifestParser.parse_file("examples/fixtures/cawg_manifest_c2pa.json")
print(signal.parser_mode)   # c2pa_json
print(signal.actor_id)      # did:web:publisher.example
print(signal.action)        # publish
```

## Step 2: Build a verification request

Use the fixture loader when you want a deterministic request object from either input shape.

```python
from cawg_trqp_refimpl.fixture_loader import load_manifest_fixture

request = load_manifest_fixture(
    "examples/fixtures/cawg_manifest_c2pa.json",
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
print(result.policy_freshness)  # snapshot_verified
```

### Edge trust path

For edge verification, the verifier now enforces this order:

1. load snapshot
2. verify Ed25519 signature using trust anchors
3. enforce `expires_at`
4. evaluate authorization and recognition from snapshot data
5. return `trusted_cached`, `rejected`, or `deferred`

## Snapshot signing workflow

```bash
python scripts/sign_snapshot.py \
  data/snapshot.json \
  data/snapshot_signing_key.example.pem \
  --key-id media-registry-snapshot-key-1
```

This repo includes:

- `data/snapshot.json` as a signed example snapshot
- `data/trust_anchors.json` as the verifier trust-anchor set
- `data/snapshot_signing_key.example.pem` as an example signing key for local experimentation

## HTTP mode

```bash
python scripts/start_http_service.py --host 0.0.0.0 --port 5000
```

The HTTP service continues to expose:

- `POST /trqp/authorization`
- `POST /trqp/recognition`
- `GET /health`

## Outcome interpretation

| Field | Meaning |
|---|---|
| `trust_outcome` | trusted, trusted_cached, rejected, or deferred |
| `actor_authorization` | authorized, not_authorized, or unknown |
| `issuer_recognition` | recognized or unknown |
| `policy_freshness` | current, snapshot_verified, missing_snapshot, expired_snapshot, etc. |
| `verification_mode` | cached_online, online_full, offline_snapshot, or revocation_check |
