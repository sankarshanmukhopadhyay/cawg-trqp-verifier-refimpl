# Reproducibility Guide

The canonical reproducibility fixture remains:

- `examples/reproducibility_bundle_standard.json`

In `v0.12.0`, reproducibility now includes the resolved profile object carried in `replay_inputs.profile`.

## Validate

```bash
python scripts/check_reproducibility.py examples/reproducibility_bundle_standard.json
```

## What is being compared

The comparison now covers:

- request payload
- resolved verification profile
- policy and recognition evidence
- process appraisal
- verification result
- deterministic bundle digest
