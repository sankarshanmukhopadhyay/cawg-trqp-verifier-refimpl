.PHONY: validate flagship-check

# Authoritative repository completion gate. CI MUST invoke this target rather
# than maintain an independent validator list.
validate:
	python scripts/validate_repository.py
	python scripts/validate_portfolio_contract.py
	python scripts/validate_api_contract.py
	python scripts/validate_examples.py
	python scripts/validate_walkthrough_examples.py
	python scripts/validate_walkthrough_diagrams.py
	python scripts/validate_walkthrough_quality.py
	python scripts/validate_agentic_assurance.py
	python scripts/validate_adoption_journeys.py
	python scripts/validate_learning_paths.py
	python scripts/validate_feed_descriptors.py
	python scripts/validate_audit_bundle.py examples/exported_audit_bundle.signed.json --trust-anchors data/trust_anchors.json
	python scripts/replay_audit_bundle.py examples/reproducibility_bundle_standard.json --trusted-root .
	python scripts/validate_photography_contest_example.py
	python scripts/export_conformance_pack.py --check
	python scripts/generate_release_checksums.py --check
	pytest -q

flagship-check:
	python scripts/validate_repository.py
	python scripts/validate_portfolio_contract.py
