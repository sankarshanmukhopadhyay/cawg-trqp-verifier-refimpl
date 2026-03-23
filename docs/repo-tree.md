# Repository Tree

```text
.
├── README.md
├── LICENSE
├── CHANGELOG.md
├── ROADMAP.md
├── RELEASE_NOTES_v0.3.0.md
├── RELEASE_NOTES_v0.3.1.md
├── RELEASE_NOTES_v0.4.0.md
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── INTEGRATION_GUIDE.md
│   ├── architecture.md
│   ├── implementation-notes.md
│   ├── release-assets.md
│   ├── release-readiness.md
│   ├── repo-tree.md
│   └── verifier-profiles.md
├── issues/
│   ├── 001-real-cawg-c2pa-parser.md
│   ├── 002-signed-policy-snapshots.md
│   ├── 003-http-trqp-service.md
│   ├── 004-revocation-delta-channel.md
│   └── 005-conformance-suite-expansion.md
├── examples/
│   ├── verification_request.json
│   ├── fixtures/
│   │   ├── cawg_manifest_blocked.json
│   │   ├── cawg_manifest_c2pa.json
│   │   ├── cawg_manifest_minimal.json
│   │   └── content_bundle_example.json
│   └── expected/
│       ├── edge_result.json
│       └── standard_result.json
├── data/
│   ├── policies.json
│   ├── revocations.json
│   ├── snapshot.json
│   ├── snapshot_signing_key.example.pem
│   └── trust_anchors.json
├── schemas/
│   ├── authorization-request.schema.json
│   ├── authorization-response.schema.json
│   ├── verification-request.schema.json
│   └── verification-result.schema.json
├── src/
│   ├── cawg_trqp_refimpl/
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── cli.py
│   │   ├── context.py
│   │   ├── fixture_loader.py
│   │   ├── http_service.py
│   │   ├── manifest_parser.py
│   │   ├── mock_service.py
│   │   ├── models.py
│   │   ├── snapshot.py
│   │   └── verifier.py
│   └── cawg_trqp_refimpl.egg-info/
└── tests/
    ├── test_cache.py
    ├── test_conformance_vectors.py
    ├── test_fixture_loader.py
    ├── test_http_service.py
    ├── test_snapshot.py
    └── test_verifier.py
```
