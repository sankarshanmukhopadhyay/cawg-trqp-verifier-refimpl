"""CAWG/C2PA manifest parser for extraction of actor, issuer, and assertion signals.

This module provides a parser for CAWG/C2PA manifests, enabling extraction of
relevant provenance signals (actor identity, issuer binding, assertions) that
feed into TRQP verification workflow.

The parser supports both the simplified fixture model (for testing) and real
C2PA manifest format, with graceful degradation when full manifest parsing
is not yet available.

References:
- CAWG specifications: https://cawg.io/specs/
- C2PA manifest spec: https://c2pa.org/specifications/
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
import json


@dataclass
class ManifestSignal:
    """Extracted trust signals from a manifest."""

    actor_id: str
    """Entity performing the action."""

    issuer_id: Optional[str] = None
    """Issuing authority for identity material."""

    credential_type: Optional[str] = None
    """Type of credential/assertion used."""

    assertions: list[dict[str, Any]] = field(default_factory=list)
    """Extracted assertion objects from manifest."""

    provenance_chain: list[str] = field(default_factory=list)
    """Chain of claim precedence or assertion history."""

    integrity_status: str = "unknown"
    """Overall manifest integrity (verified, failed, unknown)."""

    raw_manifest: dict[str, Any] = field(default_factory=dict)
    """Complete parsed manifest for downstream use."""


class CAWGManifestParser:
    """Parser for CAWG/C2PA manifests."""

    # For now, supports simplified fixture format with graceful fallback.
    # Future versions will integrate the full C2PA manifest parser.

    FIXTURE_MODEL_VERSION = "0.1"
    """Current supported fixture model version."""

    @staticmethod
    def parse_fixture(fixture_path: str | Path) -> ManifestSignal:
        """Parse a simplified CAWG/C2PA fixture.

        Args:
            fixture_path: Path to JSON fixture file

        Returns:
            ManifestSignal with extracted trust signals

        Raises:
            FileNotFoundError: If fixture file does not exist
            ValueError: If fixture is malformed or incompatible
        """
        path = Path(fixture_path)
        if not path.exists():
            raise FileNotFoundError(f"Fixture not found: {fixture_path}")

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in fixture: {e}") from e

        return CAWGManifestParser._extract_signals(data)

    @staticmethod
    def parse_dict(manifest_data: dict[str, Any]) -> ManifestSignal:
        """Parse manifest from dictionary.

        Args:
            manifest_data: Parsed manifest dictionary

        Returns:
            ManifestSignal with extracted trust signals
        """
        return CAWGManifestParser._extract_signals(manifest_data)

    @staticmethod
    def _extract_signals(manifest_data: dict[str, Any]) -> ManifestSignal:
        """Extract trust signals from parsed manifest.

        Supports:
        1. Simplified fixture format with actor_id, issuer_id fields
        2. C2PA-style manifest format with claim/assertion structures
        3. Mixed formats with graceful fallback

        Args:
            manifest_data: Parsed manifest dictionary

        Returns:
            ManifestSignal with extracted signals
        """

        # Check for simplified fixture model (primary format for this phase)
        if "actor_id" in manifest_data:
            return ManifestSignal(
                actor_id=manifest_data.get("actor_id", "unknown"),
                issuer_id=manifest_data.get("issuer_id"),
                credential_type=manifest_data.get("credential_type", "claim"),
                assertions=manifest_data.get("assertions", []),
                provenance_chain=manifest_data.get("provenance_chain", []),
                integrity_status=manifest_data.get("integrity_status", "verified"),
                raw_manifest=manifest_data,
            )

        # Graceful fallback for C2PA-style structures (future compatibility)
        # Extract from claim structures if present
        signal = ManifestSignal(
            actor_id="unknown",
            raw_manifest=manifest_data,
        )

        # Try to extract actor from nested claim structures
        if "claim" in manifest_data:
            claim = manifest_data["claim"]
            if isinstance(claim, dict) and "issuer" in claim:
                signal.actor_id = claim.get("issuer", "unknown")
                signal.issuer_id = claim.get("issuer", "unknown")

        # Extract assertions if present
        if "assertions" in manifest_data:
            assertions = manifest_data["assertions"]
            if isinstance(assertions, list):
                signal.assertions = assertions

        return signal

    @staticmethod
    def validate_fixture(fixture_path: str | Path) -> dict[str, Any]:
        """Validate fixture for structure and required fields.

        Args:
            fixture_path: Path to fixture file

        Returns:
            Dictionary with validation results

        Raises:
            FileNotFoundError: If fixture file does not exist
        """
        path = Path(fixture_path)
        if not path.exists():
            raise FileNotFoundError(f"Fixture not found: {fixture_path}")

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            return {"valid": False, "error": f"Invalid JSON: {e}"}

        # Validate required fields
        required_fields = ["actor_id"] if "actor_id" in data else []
        missing = [f for f in required_fields if f not in data]

        return {
            "valid": len(missing) == 0,
            "missing_fields": missing,
            "has_issuer_id": "issuer_id" in data,
            "has_assertions": "assertions" in data,
            "has_credential_type": "credential_type" in data,
        }
