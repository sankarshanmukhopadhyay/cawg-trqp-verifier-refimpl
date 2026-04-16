# Verifier Profiles

## Purpose

Verifier profiles are machine-readable enforcement contracts.

They govern not only verification behavior, but also transport posture, revocation freshness, failure handling, evidence expectations, and replayability.

## Control model

A profile contains the following control groups:

- `authority`
- `freshness`
- `revocation`
- `failure`
- `evidence`
- `transport`
- `determinism`

## Transport controls

```json
{
  "transport": {
    "mode": "http",
    "integrity": "tls",
    "availability_requirement": "best_effort"
  }
}
```

These controls express what the profile is willing to trust about the policy feed path.

## Revocation controls

```json
{
  "revocation": {
    "mode": "delta",
    "hard_fail": false,
    "max_age_seconds": 3600,
    "enforcement": "warn",
    "delta_channel_required": false
  }
}
```

These controls express how revocation freshness is judged and whether stale material causes warning or failure.

## Determinism controls

```json
{
  "determinism": {
    "replayable": true,
    "require_pinned_feeds": false
  }
}
```

These controls matter for replay and fixture exchange. They tell downstream systems whether the profile expects pinned policy inputs as part of a credible reproduction story.

## Built-in profiles

### `edge`

- local signed snapshot posture
- no live network required
- snapshot-oriented evidence surface
- intended for offline or constrained deployments

### `standard`

- cache-first verification with live fallback
- HTTP/TLS transport accepted and gateway-compatible
- warning-oriented revocation freshness posture
- replayable and suitable for baseline interoperability work

### `high_assurance`

- live policy posture
- required transport availability
- hard-fail semantics for revocation freshness breaches
- attested audit bundle expectations
- pinned-feed replay expectations

## Overlay model

The governing unit remains:

```text
verification_profile = base_profile + assurance_overlay(s)
```

Overlays allow stricter freshness and evidence semantics without multiplying base profile names. That keeps the profile system legible while still letting assurance programs express stronger requirements.
