---
layout: default
title: "External C2PA Validation Boundary"
parent: "Implementation Guides"
nav_order: 6
---
# External C2PA validation: opt-in feasibility boundary

**Status:** experimental adapter; no adopted CAWG Delegated Creator interoperability or conformance claim.

The [official c2patool](https://github.com/contentauth/c2patool) CLI can validate binary C2PA assets. This repository exposes a bounded, **optional** adapter in `src/cawg_trqp_refimpl/external_c2pa_validation.py` producing a typed receipt. It **does not** reinterpret that receipt as issuer identity, delegated authority, trusted signing time or TRQP response.

## Reproduce

Install `c2patool` separately according to the upstream project and obtain a legally redistributable real signed C2PA asset. Execute:

```python
from cawg_trqp_refimpl.external_c2pa_validation import validate_c2pa_asset
receipt = validate_c2pa_asset("path/to/signed-asset.jpg")
print(receipt)
```

The runtime has a 30-second timeout, at most 4 MiB of captured output per stream, never invokes a shell, and never downloads content. By default, no trust anchors are configured and signer trust is **not evaluated**. The binary tool must already be available on PATH. Configure and pin trust bundles separately under the operator's trust policy; do not silently fetch external trust lists during verification. A valid manifest is not proof of delegated authority.

### Assurance

`manifest_integrity` can be `validated_by_external_tool`, `failed` or `indeterminate`. It only becomes positive when the external tool exits successfully, publishes explicit empty `validation_status`, and names an active manifest. Missing status or tool, malformed output, or timeout fail closed as indeterminate. A nonzero exit or recorded validator failures produces `failed`. `signer_trust`, `delegated_authority`, and `trusted_signing_time` stay `not_evaluated` irrespective of validity.

**Important:** The tests mock the CLI and do **not** establish successful validation against a real signed asset, C2PA trust list, or TRQP v2 registry. This is an executable integration seam, not completed independent interoperability. Do not mark TF-07 or Issue #75 completed based on mock tests.

### Next evidence gate

Supply a pinned tool version, license-cleared real signed positive/negative assets, pinned trust-list fingerprint, a reachable representative TRQP v2.0 authorization/recognition endpoint, and a repeatable recorded execution. Evidence receipts must name origin, trust anchors, failure distinctions and reproducibility metadata. The Taskforce's proposed profile remains non-normative until CAWG acts.
