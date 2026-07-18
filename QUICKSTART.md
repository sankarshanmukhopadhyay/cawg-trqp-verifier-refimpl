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
