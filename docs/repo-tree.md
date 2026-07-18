---
layout: default
title: "Repository Tree"
description: "Machine-generated file tree of the repository."
parent: "Architecture & Deployment"
nav_order: 7
---

# Repository Tree

```text
.
├── .github
│   ├── ISSUE_TEMPLATE
│   │   ├── adoption_report.yml
│   │   ├── bug_report.yml
│   │   └── config.yml
│   ├── workflows
│   │   ├── ci.yml
│   │   ├── pages.yml
│   │   └── pypi-publish.yml
│   ├── dependabot.yml
│   └── pull_request_template.md
├── conformance
│   ├── assurance-suite-manifest.json
│   ├── compatibility-matrix.json
│   └── risk-to-test-map.yaml
├── data
│   ├── policies.json
│   ├── policies_multi_authority.json
│   ├── repository-metadata.yaml
│   ├── revocations.json
│   ├── snapshot.json
│   ├── snapshot_signing_key.example.pem
│   └── trust_anchors.json
├── docs
│   ├── sections
│   │   ├── architecture-index.md
│   │   ├── assurance-index.md
│   │   ├── governance-index.md
│   │   ├── implementation-guides-index.md
│   │   ├── interoperability-index.md
│   │   ├── releases-index.md
│   │   └── walkthroughs-index.md
│   ├── workflows
│   │   └── photography-contest-verification.md
│   ├── INTEGRATION_GUIDE.md
│   ├── NON_TECHNICAL_OVERVIEW.md
│   ├── PRESENTATION_BRIEF.md
│   ├── architecture.md
│   ├── assurance-suite-ingestion.md
│   ├── audit-bundle-profile.md
│   ├── compatibility-matrix.md
│   ├── decision-receipt-specification.md
│   ├── deployment-guide.md
│   ├── descriptor-policy.md
│   ├── deterministic-input-trust.md
│   ├── feed-descriptor-profile.md
│   ├── how-trqp-enables-assurance.md
│   ├── http-transport-patterns.md
│   ├── implementation-notes.md
│   ├── index.md
│   ├── interoperability-vectors.md
│   ├── operational-hardening.md
│   ├── parser-adapter-contract.md
│   ├── release-assets.md
│   ├── release-readiness.md
│   ├── repo-tree.md
│   ├── reproducibility-guide.md
│   ├── risk-crosswalk.md
│   ├── trqp-adoption-path.md
│   ├── trqp-alignment.md
│   ├── trust-gateway.md
│   ├── verifier-profiles.md
│   └── video-verification-walkthrough.md
├── examples
│   ├── decision_receipts
│   │   ├── README.md
│   │   ├── decision_receipt_edge.json
│   │   ├── decision_receipt_high_assurance.json
│   │   └── decision_receipt_standard.json
│   ├── expected
│   │   ├── edge_result.json
│   │   └── standard_result.json
│   ├── feed_descriptors
│   │   ├── gateway-route-feed.signed.json
│   │   ├── policy-feed.signed.json
│   │   ├── revocation-feed.signed.json
│   │   └── snapshot-feed.signed.json
│   ├── fixtures
│   │   ├── cawg_manifest_blocked.json
│   │   ├── cawg_manifest_c2pa.json
│   │   ├── cawg_manifest_c2pa_pop.json
│   │   ├── cawg_manifest_c2pa_pop_failed.json
│   │   ├── cawg_manifest_minimal.json
│   │   └── content_bundle_example.json
│   ├── photography_contest
│   │   ├── README.md
│   │   ├── contest_policy_feed.json
│   │   ├── contest_revocation_feed.json
│   │   ├── decision_receipt.json
│   │   ├── policy-feed.signed.json
│   │   ├── replay_bundle.json
│   │   ├── revocation-feed.signed.json
│   │   ├── submission.json
│   │   └── trust_anchors.json
│   ├── benchmark_constrained_device_request.json
│   ├── benchmark_high_volume_request.json
│   ├── exported_audit_bundle.json
│   ├── exported_audit_bundle.signed.json
│   ├── interoperability_vector_gateway.json
│   ├── interoperability_vector_multi_authority.json
│   ├── reproducibility_bundle_standard.json
│   └── verification_request.json
├── fixtures
│   ├── profile-bound
│   │   ├── gateway-standard-v1
│   │   │   ├── pinned_feeds
│   │   │   │   ├── policies.json
│   │   │   │   └── revocations.json
│   │   │   ├── expected_result.json
│   │   │   ├── manifest.json
│   │   │   ├── request.json
│   │   │   └── resolved_profile.json
│   │   ├── high-assurance-v1
│   │   │   ├── pinned_feeds
│   │   │   │   ├── policies.json
│   │   │   │   └── revocations.json
│   │   │   ├── expected_result.json
│   │   │   ├── manifest.json
│   │   │   ├── request.json
│   │   │   └── resolved_profile.json
│   │   ├── multi-authority-v1
│   │   │   ├── pinned_feeds
│   │   │   │   ├── policies.json
│   │   │   │   └── revocations.json
│   │   │   ├── expected_result.json
│   │   │   ├── manifest.json
│   │   │   ├── request.json
│   │   │   └── resolved_profile.json
│   │   └── standard-v1
│   │       ├── pinned_feeds
│   │       │   ├── policies.json
│   │       │   └── revocations.json
│   │       ├── expected_result.json
│   │       ├── manifest.json
│   │       ├── request.json
│   │       └── resolved_profile.json
│   └── README.md
├── issues
│   ├── 001-real-cawg-c2pa-parser.md
│   ├── 002-signed-policy-snapshots.md
│   ├── 003-http-trqp-service.md
│   ├── 004-revocation-delta-channel.md
│   └── 005-conformance-suite-expansion.md
├── profiles
│   ├── overlays
│   │   ├── evidence_attested.json
│   │   └── freshness_strict.json
│   ├── edge.json
│   ├── high_assurance.json
│   └── standard.json
├── release-assets
│   ├── checksums-v0.16.0.json
│   └── checksums-v0.17.0.json
├── schemas
│   ├── audit-bundle.schema.json
│   ├── authorization-request.schema.json
│   ├── authorization-response.schema.json
│   ├── decision-receipt.schema.json
│   ├── feed-attestation.schema.json
│   ├── feed-descriptor.schema.json
│   ├── verification-profile.schema.json
│   ├── verification-request.schema.json
│   └── verification-result.schema.json
├── scripts
│   ├── check_reproducibility.py
│   ├── export_conformance_pack.py
│   ├── export_repo_tree.py
│   ├── generate_release_checksums.py
│   ├── replay_audit_bundle.py
│   ├── run_demo.py
│   ├── sign_audit_bundle.py
│   ├── sign_snapshot.py
│   ├── start_http_service.py
│   ├── validate_audit_bundle.py
│   ├── validate_examples.py
│   ├── validate_feed_descriptors.py
│   ├── validate_photography_contest_example.py
│   └── validate_repository.py
├── src
│   └── cawg_trqp_refimpl
│       ├── __init__.py
│       ├── attestation.py
│       ├── audit.py
│       ├── cache.py
│       ├── cli.py
│       ├── context.py
│       ├── feed_descriptor.py
│       ├── fixture_loader.py
│       ├── gateway.py
│       ├── http_service.py
│       ├── jsoncanon.py
│       ├── manifest_adapters.py
│       ├── manifest_parser.py
│       ├── mock_service.py
│       ├── models.py
│       ├── profile.py
│       ├── replay.py
│       ├── snapshot.py
│       ├── transport.py
│       ├── validation.py
│       └── verifier.py
├── tests
│   ├── test_audit_bundle.py
│   ├── test_cache.py
│   ├── test_conformance_vectors.py
│   ├── test_decision_receipt_reason_codes.py
│   ├── test_feed_descriptor_conformance_vectors.py
│   ├── test_feed_descriptors.py
│   ├── test_fixture_loader.py
│   ├── test_fixture_packages.py
│   ├── test_gateway_routes.py
│   ├── test_http_service.py
│   ├── test_http_service_integration.py
│   ├── test_photography_contest_example.py
│   ├── test_profiles.py
│   ├── test_replay_feed_descriptor_evidence.py
│   ├── test_security_hardening.py
│   ├── test_snapshot.py
│   ├── test_transport_and_replay_fidelity.py
│   └── test_verifier.py
├── .gitignore
├── CHANGELOG.md
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── Dockerfile
├── GITHUB_RELEASE_TEMPLATE.md
├── GOVERNANCE.md
├── Gemfile
├── LICENSE
├── Makefile
├── QUICKSTART.md
├── README.md
├── RELEASE_NOTES_v0.11.0.md
├── RELEASE_NOTES_v0.12.0.md
├── RELEASE_NOTES_v0.13.0.md
├── RELEASE_NOTES_v0.14.0.md
├── RELEASE_NOTES_v0.15.0.md
├── RELEASE_NOTES_v0.16.0.md
├── RELEASE_NOTES_v0.17.0.md
├── RELEASE_NOTES_v0.3.0.md
├── RELEASE_NOTES_v0.3.1.md
├── RELEASE_NOTES_v0.4.0.md
├── RELEASE_NOTES_v0.5.0.md
├── RELEASE_NOTES_v0.7.0.md
├── RELEASE_NOTES_v0.9.0.md
├── ROADMAP.md
├── SECURITY.md
├── _config.yml
├── docker-compose.yml
├── pyproject.toml
├── requirements-lock.txt
└── requirements.txt
```
