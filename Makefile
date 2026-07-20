.PHONY: validate flagship-check

validate:
	python scripts/validate_repository.py
	python scripts/validate_api_contract.py
	python scripts/validate_examples.py
	pytest -q

flagship-check:
	python scripts/validate_repository.py
