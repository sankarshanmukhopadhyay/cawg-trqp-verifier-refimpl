# Repository Tree

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── conformance/
│   ├── assurance-suite-manifest.json
│   ├── compatibility-matrix.json
│   └── risk-to-test-map.yaml
├── data/
│   ├── policies.json
│   ├── policies_multi_authority.json
│   ├── revocations.json
│   ├── snapshot.json
│   ├── snapshot_signing_key.example.pem
│   └── trust_anchors.json
├── docs/
│   ├── assurance-suite-ingestion.md
│   ├── descriptor-policy.md
│   ├── operational-hardening.md
│   ├── parser-adapter-contract.md
│   ├── release-readiness.md
│   └── workflows/
├── examples/
│   ├── decision_receipts/
│   ├── feed_descriptors/
│   ├── fixtures/
│   ├── photography_contest/
│   ├── exported_audit_bundle.json
│   ├── exported_audit_bundle.signed.json
│   └── reproducibility_bundle_standard.json
├── fixtures/
│   └── profile-bound/
│       ├── gateway-standard-v1/
│       ├── high-assurance-v1/
│       ├── multi-authority-v1/
│       └── standard-v1/
├── issues/
│   ├── 001-real-cawg-c2pa-parser.md
│   ├── 002-signed-policy-snapshots.md
│   ├── 003-http-trqp-service.md
│   ├── 004-revocation-delta-channel.md
│   └── 005-conformance-suite-expansion.md
├── profiles/
│   ├── overlays/
│   ├── edge.json
│   ├── high_assurance.json
│   └── standard.json
├── release-assets/
│   └── checksums-v0.16.0.json
├── schemas/
├── scripts/
│   ├── export_conformance_pack.py
│   ├── generate_release_checksums.py
│   ├── replay_audit_bundle.py
│   └── validate_*.py
├── src/
│   └── cawg_trqp_refimpl/
│       ├── manifest_adapters.py
│       ├── profile.py
│       ├── verifier.py
│       └── ...
├── tests/
├── CHANGELOG.md
├── GITHUB_COMMIT_MESSAGE_v0.16.0.md
├── README.md
├── RELEASE_NOTES_v0.16.0.md
├── ROADMAP.md
├── pyproject.toml
├── requirements-lock.txt
└── requirements.txt
```
