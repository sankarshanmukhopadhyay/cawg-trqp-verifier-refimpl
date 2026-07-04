"""Manifest parser adapter contract for CAWG/C2PA signal extraction."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .manifest_parser import CAWGManifestParser, ManifestSignal


class ManifestParserAdapter(Protocol):
    """Stable adapter interface for manifest signal extraction backends."""

    adapter_id: str

    def parse_file(self, manifest_path: str | Path) -> ManifestSignal:
        """Extract verifier-ready signals from a manifest file."""


class JsonManifestAdapter:
    """Adapter for repository JSON fixtures and C2PA-style JSON envelopes."""

    adapter_id = "json-fixture-v1"

    def parse_file(self, manifest_path: str | Path) -> ManifestSignal:
        return CAWGManifestParser.parse_file(manifest_path)


class C2PABinaryManifestAdapter:
    """Reserved adapter boundary for binary C2PA extraction libraries."""

    adapter_id = "c2pa-binary-v1"

    def parse_file(self, manifest_path: str | Path) -> ManifestSignal:
        raise RuntimeError(
            "binary C2PA parsing is not bundled; install and wire a supported "
            "C2PA extraction backend behind ManifestParserAdapter"
        )
