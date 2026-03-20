# CAWG–TRQP Integration Guide

## Overview

This reference implementation demonstrates how TRQP (Trust Registry Query Protocol) functions as the **governance decision plane** in a CAWG/C2PA (Content Authenticity and Provenance) verification workflow.

## Architectural Separation of Concerns

The CAWG–TRQP stack cleanly divides verification labor:

| Component | Responsibility | Reference |
|-----------|-----------------|-----------|
| **CAWG/C2PA** | Content provenance and assertion binding | https://cawg.io/specs/ |
| **Identity Material** | Actor and issuer binding (DIDs, certificates) | https://cawg.io/specs/ |
| **TRQP** | Authorization and issuer recognition queries | https://trustoverip.github.io/tswg-trust-registry-protocol/ |
| **Verifier** | Orchestration and trust synthesis | This repository |

## Verification Workflow

### Step 1: Extract Signals from Manifest

Parse the CAWG/C2PA manifest to extract:
- **Actor ID**: Entity performing the signing/authorization
- **Issuer ID**: Authority that issued credentials
- **Assertions**: Content, timestamp, and provenance claims

```python
from cawg_trqp_refimpl.manifest_parser import CAWGManifestParser

signal = CAWGManifestParser.parse_fixture("path/to/manifest.json")
print(f"Actor: {signal.actor_id}")
print(f"Issuer: {signal.issuer_id}")
print(f"Assertions: {signal.assertions}")
```

### Step 2: Construct Verification Request

Build a TRQP-compatible verification request with extracted signals:

```python
from cawg_trqp_refimpl.models import VerificationRequest

request = VerificationRequest(
    entity_id=signal.actor_id,
    issuer_id=signal.issuer_id,
    authority_id="did:web:trust-authority.example",  # Your trust registry
    action="verify",
    resource="manifest",
    context={
        "credential_type": signal.credential_type or "claim",
        "assertion_count": len(signal.assertions),
    },
    integrity_ok=True,  # Set based on content hash validation
)
```

### Step 3: Choose Verification Profile

Select a profile based on network and assurance requirements:

| Profile | Mode | Network | Cache | Use Case |
|---------|------|---------|-------|----------|
| **edge** | snapshot-only | offline/intermittent | offline store | handheld, constrained devices, disconnected verification |
| **standard** | cache-first + live on miss | stable | TTL cache | platform and service verification |
| **high_assurance** | live-only | stable | none | regulated, audit-required, high-assurance verification |

```python
# Choose based on deployment context
profile = "standard"  # or "edge" or "high_assurance"
```

### Step 4: Verify with Orchestrator

Create a verifier and run verification:

```python
from cawg_trqp_refimpl.verifier import Verifier
from cawg_trqp_refimpl.mock_service import MockTRQPService
from cawg_trqp_refimpl.snapshot import SnapshotStore

# Option A: Online verification (standard or high_assurance)
verifier = Verifier(
    service=MockTRQPService(
        policy_path="data/policies.json",
        revocation_path="data/revocations.json",
    )
)

# Option B: Offline verification (edge)
verifier = Verifier(
    snapshot=SnapshotStore("data/snapshot.json")
)

# Option C: Hybrid (cache + snapshot)
verifier = Verifier(
    service=MockTRQPService("data/policies.json"),
    snapshot=SnapshotStore("data/snapshot.json"),
)

result = verifier.verify(request, profile=profile)
```

### Step 5: Interpret Trust Outcome

The verifier returns a `VerificationResult` with structured signals:

```python
print(f"Trust outcome: {result.trust_outcome}")  # trusted, rejected, deferred, trusted_cached
print(f"Asset integrity: {result.asset_integrity}")  # verified, failed
print(f"Authorization: {result.actor_authorization}")  # authorized, not_authorized, unknown
print(f"Recognition: {result.issuer_recognition}")  # recognized, unknown
print(f"Policy freshness: {result.policy_freshness}")  # current, snapshot, revoked, service_unavailable
print(f"Mode: {result.verification_mode}")  # online_full, cached_online, offline_snapshot, revocation_check
```

## Usage Modes

### Mode 1: In-Process Verification

Use the mock TRQP service for testing and standalone verification:

```python
from cawg_trqp_refimpl.verifier import Verifier
from cawg_trqp_refimpl.mock_service import MockTRQPService

verifier = Verifier(
    service=MockTRQPService("data/policies.json")
)
result = verifier.verify(request, profile="standard")
```

### Mode 2: HTTP Network Service

Expose TRQP endpoints over HTTP for distributed verification:

```bash
# Start the service
python scripts/start_http_service.py --host 0.0.0.0 --port 5000

# Query endpoints
curl -X POST http://localhost:5000/trqp/authorization \
  -H "Content-Type: application/json" \
  -d '{
    "entity_id": "did:web:example.com",
    "authority_id": "did:web:trust-authority.example",
    "action": "verify",
    "resource": "manifest",
    "context": {}
  }'
```

Or use in Python:

```python
import requests

response = requests.post(
    "http://localhost:5000/trqp/authorization",
    json={
        "entity_id": "did:web:example.com",
        "authority_id": "did:web:trust-authority.example",
        "action": "verify",
        "resource": "manifest",
        "context": {}
    }
)
print(response.json())
```

### Mode 3: Snapshot-Based (Edge) Verification

For offline and disconnected scenarios:

```python
from cawg_trqp_refimpl.verifier import Verifier
from cawg_trqp_refimpl.snapshot import SnapshotStore

# Load a signed policy snapshot taken during connected operation
verifier = Verifier(
    snapshot=SnapshotStore("data/snapshot.json")
)
result = verifier.verify(request, profile="edge")
```

## Revocation and Policy Updates

### Applying Revocation Deltas

When entities are revoked, apply a delta update:

```python
verifier.apply_revocation_delta(
    revoked_entities=["did:web:bad-actor.example"],
    policy_epoch="2026-Q1"
)

# Subsequent verifications will reject revoked entities
result = verifier.verify(request)
# result.trust_outcome == "rejected" if entity is revoked
```

### Cache Management

Control cache behavior for high-volume scenarios:

```python
from cawg_trqp_refimpl.cache import TTLCache

cache = TTLCache()
verifier = Verifier(service=service, cache=cache)

# Cache is automatic; inspect for debugging
cached_auth = cache.get("entity_id:authority_id:action:resource:{}")
```

## Policy Data Format

### Policies (policies.json)

```json
{
  "authorization": [
    {
      "entity_id": "did:web:example.com",
      "authority_id": "did:web:authority.example",
      "action": "verify",
      "resource": "manifest",
      "context": {},
      "authorized": true,
      "expires": "2026-12-31T23:59:59Z",
      "policy_epoch": "2026-Q1",
      "evidence": ["signature", "credential"],
      "reason": "trusted_issuer"
    }
  ],
  "recognition": [
    {
      "authority_id": "did:web:authority.example",
      "recognized_authority_id": "did:web:other-authority.example",
      "context": {},
      "recognized": true,
      "expires": "2026-12-31T23:59:59Z",
      "policy_epoch": "2026-Q1"
    }
  ]
}
```

### Snapshots (snapshot.json)

Offline policy state captured at a point in time:

```json
{
  "captured_at": "2026-03-20T00:00:00Z",
  "policy_epoch": "2026-Q1",
  "signature": "...",
  "data": {
    "authorization": [...],
    "recognition": [...]
  }
}
```

### Revocations (revocations.json)

Delta updates to block entities:

```json
{
  "revoked_entities": ["did:web:blocked.example"],
  "policy_epoch": "2026-Q1"
}
```

## Testing and Conformance

### Run Conformance Suite

```bash
pytest tests/test_conformance_vectors.py -v
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Demo

```bash
python scripts/run_demo.py
```

## Integration Checklist

- [ ] Extract signals from manifest (actor_id, issuer_id, assertions)
- [ ] Build VerificationRequest with extracted signals
- [ ] Choose profile (edge/standard/high_assurance)
- [ ] Create Verifier with service and/or snapshot
- [ ] Call verify() and interpret trust_outcome
- [ ] Apply revocation deltas as needed
- [ ] Log/audit verification results for compliance
- [ ] Monitor cache hit rates and performance

## Next Steps

For production deployment:

1. **Real C2PA Parser**: Integrate c2pa-python library for production manifests
2. **Signed Snapshots**: Add cryptographic verification of snapshot signatures
3. **Service Scaling**: Deploy HTTP service behind load balancer
4. **Policy Management**: Integrate with policy backend (database, Git, etc.)
5. **Audit Logging**: Add structured logging for compliance
6. **Metrics**: Add Prometheus/StatsD instrumentation

## References

- **CAWG Specifications**: https://cawg.io/specs/
- **TRQP v2.0 Specification**: https://trustoverip.github.io/tswg-trust-registry-protocol/
- **C2PA Manifest Format**: https://c2pa.org/specifications/
- **DIDs (Decentralized Identifiers)**: https://www.w3.org/TR/did-core/
- **Verifiable Credentials**: https://www.w3.org/TR/vc-data-model/
