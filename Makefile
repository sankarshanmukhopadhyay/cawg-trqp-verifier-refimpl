.PHONY: validate flagship-check

validate:
	python scripts/validate_repository.py
	python scripts/validate_portfolio_contract.py
	python scripts/validate_api_contract.py
	python scripts/validate_examples.py
	python scripts/validate_walkthrough_examples.py
	python scripts/validate_walkthrough_diagrams.py
	python scripts/validate_walkthrough_quality.py
	python scripts/validate_agentic_assurance.py
	pytest -q

flagship-check:
	python scripts/validate_repository.py
	python scripts/validate_portfolio_contract.py
