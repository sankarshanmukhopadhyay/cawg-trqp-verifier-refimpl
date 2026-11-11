---
layout: default
title: "Quickstart"
description: "Get a first verification result in under ten minutes."
nav_order: 3
---
# Quickstart

## Install

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-lock.txt
pip install -e .
```

## Run a verification

```bash
python -m cawg_trqp_refimpl.cli examples/verification_request.json --profile standard
```

## Validate the repository

```bash
make validate
```

A successful run produces a structured verification result. Replay and audit-bundle examples are documented in `docs/reproducibility-guide.md` and `docs/audit-bundle-profile.md`.

## Experimental consent-evidence demonstration (v0.21.0)

The repository provides a separate, synthetic consent-claim evaluator for cross-taskforce assurance research. It is not a consent authenticator, rights service, or legal permission determination. After installing the package, run:

```bash
python scripts/run_taskforce_consent_demo.py
pytest -q tests/test_experimental_consent_assurance.py tests/test_experimental_consent_temporal.py tests/test_taskforce_consent_scenarios.py
```

Results retain `assured_consent=indeterminate` and `assured_authority=indeterminate` even when caller-supplied claims are internally consistent. See [the experimental boundary](docs/agentic-ai/experimental-consent-assurance.md).
