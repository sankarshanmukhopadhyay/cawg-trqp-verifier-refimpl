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

## Independent real-asset evidence acceptance (Session 4 follow-up)

The Taskforce's Q13 request for signed test files and a trusted root is an
**external evidence dependency**, not an implementation pass. Record each
independently supplied candidate with a permitted testing/redistribution
licence, immutable file digest, source, acquisition date, pinned c2patool
version and execution environment. Supply both a valid signed asset and an
adversarial counterpart (for example, an intentionally altered signed asset).
Do not commit private agreements, identity mappings or non-redistributable
media. Test assets must not use a public fixture private key as an accepted
production root.

A meaningful #75 reproduction must establish independently:

1. **C2PA path:** the external tool actually executes on the pinned asset and
   records the result, including failures, without substituting mocked output.
2. **Signer/source path:** the applicable trusted root, identity/key binding,
   recognition policy and observation time are established separately;
   `manifest_integrity=validated_by_external_tool` is insufficient.
3. **Delegation path:** the delegated terms and covered asset are actually
   bound by the relevant signatures, with action/resource/purpose and time
   checked independently. A local Ed25519 statement fixture does not prove
   CAWG assertion coverage.
4. **Consent path, when required by the use case:** the external consent
   source, its authority, record authenticity, subject binding, effective
   time and observation time are verified separately from delegation. An
   HTTPS reference and claimed digest alone never establish permission.
5. **Independent replay:** a second operator reproduces outcomes using
   pinned inputs and records discrepancies, non-positive states and source
   provenance. No synthetic PASS is counted toward independent interop.

Until these conditions have reproducible evidence, keep #75 open, preserve
`not_evaluated` and `indeterminate` states, and describe the experiment
as locally reproducible rather than externally interoperable.

The adapter computes the asset digest in fixed-size blocks to avoid a
whole-file memory allocation. The 4 MiB report limit is checked **after**
the external command returns; `subprocess.run` still captures the process
output before checking its length. Therefore this limit is not an
operating-system-level output quota. Use external process/container output
quotas for untrusted media or tools until a streaming subprocess-output
limit is implemented and tested.
