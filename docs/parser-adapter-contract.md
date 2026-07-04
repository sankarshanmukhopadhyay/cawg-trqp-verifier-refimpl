# Parser Adapter Contract

## Purpose

The verifier needs stable trust signals even when manifest extraction backends evolve. v0.16.0 adds a parser adapter boundary so JSON fixtures and future binary CAWG/C2PA extraction can share one signal contract.

The contract is implemented in:

- `src/cawg_trqp_refimpl/manifest_adapters.py`

## Adapter Interface

An adapter exposes:

```python
adapter_id: str
parse_file(manifest_path) -> ManifestSignal
```

The returned `ManifestSignal` preserves:

- actor identity
- issuer identity
- credential type
- action and resource
- context
- assertions
- provenance chain
- integrity status
- process evidence
- parser mode

## Current Adapters

| Adapter | Status | Role |
|---|---|---|
| `JsonManifestAdapter` | implemented | Parses repository JSON fixtures and C2PA-style JSON envelopes. |
| `C2PABinaryManifestAdapter` | reserved | Defines the integration boundary for a future binary C2PA extraction backend. |

## Non-Goal

v0.16.0 does not bundle a binary C2PA parser. That dependency should be introduced only when redistribution rights, deterministic validation behavior, and fixture licensing are clear.

## Assurance Rule

Parser backends may change extraction mechanics, but they must not change the verifier signal contract. External adapters should be tested against the same authorization, recognition, process evidence, and replay expectations used by the JSON adapter.
