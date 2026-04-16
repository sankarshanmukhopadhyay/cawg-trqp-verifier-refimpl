from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = PACKAGE_ROOT / "schemas" / "verification-profile.schema.json"
BUILTIN_PROFILE_DIR = PACKAGE_ROOT / "profiles"
BUILTIN_OVERLAY_DIR = BUILTIN_PROFILE_DIR / "overlays"


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(PACKAGE_ROOT.resolve()))
    except ValueError:
        return str(path)


class VerificationProfileError(ValueError):
    """Raised when a verification profile cannot be loaded or validated."""


DEFAULT_CONTROLS: dict[str, Any] = {
    "authority": {
        "trust_anchors_required": False,
        "allow_untrusted": True,
    },
    "freshness": {
        "max_age_seconds": 86400,
        "require_live": False,
    },
    "revocation": {
        "mode": "snapshot",
        "hard_fail": False,
        "max_age_seconds": 86400,
        "enforcement": "warn",
        "delta_channel_required": False,
    },
    "failure": {
        "network_failure": "fail_open",
        "policy_unavailable": "fail_open",
    },
    "evidence": {
        "emit_audit_bundle": True,
        "require_attestation": False,
    },
    "transport": {
        "mode": "local",
        "integrity": "none",
        "availability_requirement": "best_effort",
    },
    "determinism": {
        "replayable": True,
        "require_pinned_feeds": False,
    },
}


@dataclass(frozen=True)
class VerificationProfile:
    id: str
    base_profile: str
    controls: dict[str, Any]
    overlays: list[str]
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "base_profile": self.base_profile,
            "controls": deepcopy(self.controls),
            "overlays": list(self.overlays),
            "source": self.source,
        }


@dataclass(frozen=True)
class VerificationOverlay:
    id: str
    description: str
    controls: dict[str, Any]
    source: str



def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))



def _deep_merge(base: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = deepcopy(value)
    return merged



def _validator() -> Draft202012Validator:
    schema = _load_json(SCHEMA_PATH)
    return Draft202012Validator(schema)



def validate_profile_payload(payload: dict[str, Any]) -> None:
    errors = sorted(_validator().iter_errors(payload), key=lambda err: list(err.path))
    if errors:
        message = "; ".join(f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}" for err in errors)
        raise VerificationProfileError(message)



def builtin_profile_path(name: str) -> Path:
    return BUILTIN_PROFILE_DIR / f"{name}.json"



def builtin_overlay_path(name: str) -> Path:
    return BUILTIN_OVERLAY_DIR / f"{name}.json"



def load_overlay(path_or_name: str | Path) -> VerificationOverlay:
    path = Path(path_or_name)
    if not path.exists():
        path = builtin_overlay_path(str(path_or_name))
    if not path.exists():
        raise VerificationProfileError(f"Unknown overlay: {path_or_name}")
    data = _load_json(path)
    if "id" not in data or "controls" not in data:
        raise VerificationProfileError(f"Overlay {path} must include id and controls")
    return VerificationOverlay(
        id=data["id"],
        description=data.get("description", ""),
        controls=data["controls"],
        source=_display_path(path),
    )



def load_profile(profile: str | Path | dict[str, Any] | VerificationProfile, overlays: list[str | Path] | None = None) -> VerificationProfile:
    if isinstance(profile, VerificationProfile):
        if overlays:
            return apply_overlays(profile, overlays)
        return profile

    if isinstance(profile, dict):
        payload = deepcopy(profile)
        payload.setdefault("controls", deepcopy(DEFAULT_CONTROLS))
        payload["controls"] = _deep_merge(DEFAULT_CONTROLS, payload["controls"])
        payload.setdefault("overlays", [])
        payload.setdefault("source", "inline")
        validate_profile_payload(payload)
        resolved = VerificationProfile(
            id=payload["id"],
            base_profile=payload["base_profile"],
            controls=payload["controls"],
            overlays=payload.get("overlays", []),
            source=payload.get("source", "inline"),
        )
        if overlays:
            return apply_overlays(resolved, overlays)
        return resolved

    path = Path(str(profile))
    if not path.exists():
        path = builtin_profile_path(str(profile))
    if not path.exists():
        raise VerificationProfileError(f"Unknown profile: {profile}")

    data = _load_json(path)
    payload = {
        "id": data["id"],
        "base_profile": data["base_profile"],
        "controls": _deep_merge(DEFAULT_CONTROLS, data.get("controls", {})),
        "overlays": data.get("overlays", []),
        "source": _display_path(path),
    }
    validate_profile_payload(payload)
    resolved = VerificationProfile(
        id=payload["id"],
        base_profile=payload["base_profile"],
        controls=payload["controls"],
        overlays=payload["overlays"],
        source=payload["source"],
    )
    if overlays:
        return apply_overlays(resolved, overlays)
    return resolved



def apply_overlays(profile: VerificationProfile, overlays: list[str | Path]) -> VerificationProfile:
    controls = deepcopy(profile.controls)
    overlay_ids = list(profile.overlays)
    for overlay_ref in overlays:
        overlay = load_overlay(overlay_ref)
        controls = _deep_merge(controls, overlay.controls)
        overlay_ids.append(overlay.id)
    payload = {
        "id": profile.id,
        "base_profile": profile.base_profile,
        "controls": controls,
        "overlays": overlay_ids,
        "source": profile.source,
    }
    validate_profile_payload(payload)
    return VerificationProfile(
        id=payload["id"],
        base_profile=payload["base_profile"],
        controls=payload["controls"],
        overlays=overlay_ids,
        source=payload["source"],
    )
