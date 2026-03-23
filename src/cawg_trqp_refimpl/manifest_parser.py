"""CAWG/C2PA manifest parser for extraction of actor, issuer, and assertion signals.

Supports both:
- the simplified JSON fixture format used in earlier repo versions
- a real C2PA-style JSON manifest-store envelope that preserves active manifest,
  assertion labels, ingredients, and signature metadata
- process-oriented assertions that carry Proof of Process style evidence summaries
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
import json


PROCESS_ASSERTION_LABELS = {
    "cawg.process",
    "cawg.process.proof",
    "org.cawg.process",
    "org.contentauthorship.process",
}


@dataclass
class ManifestSignal:
    """Extracted trust signals from a manifest."""

    actor_id: str
    issuer_id: Optional[str] = None
    credential_type: Optional[str] = None
    assertions: list[dict[str, Any]] = field(default_factory=list)
    provenance_chain: list[str] = field(default_factory=list)
    integrity_status: str = "unknown"
    action: Optional[str] = None
    resource: Optional[str] = None
    context: dict[str, Any] = field(default_factory=dict)
    process_evidence: dict[str, Any] | None = None
    parser_mode: str = "unknown"
    raw_manifest: dict[str, Any] = field(default_factory=dict)


class CAWGManifestParser:
    """Parser for simplified fixtures and C2PA-style JSON manifests."""

    FIXTURE_MODEL_VERSION = "0.3"

    @staticmethod
    def parse_file(manifest_path: str | Path) -> ManifestSignal:
        path = Path(manifest_path)
        if not path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in manifest: {exc}") from exc
        return CAWGManifestParser.parse_dict(data)

    @staticmethod
    def parse_fixture(fixture_path: str | Path) -> ManifestSignal:
        return CAWGManifestParser.parse_file(fixture_path)

    @staticmethod
    def parse_dict(manifest_data: dict[str, Any]) -> ManifestSignal:
        if "manifest_store" in manifest_data:
            return CAWGManifestParser._extract_c2pa_manifest(manifest_data)
        return CAWGManifestParser._extract_fixture_manifest(manifest_data)

    @staticmethod
    def _extract_fixture_manifest(manifest_data: dict[str, Any]) -> ManifestSignal:
        issuer = manifest_data.get("issuer", {}) if isinstance(manifest_data.get("issuer"), dict) else {}
        actor = manifest_data.get("actor", {}) if isinstance(manifest_data.get("actor"), dict) else {}
        assertion = manifest_data.get("assertion", {}) if isinstance(manifest_data.get("assertion"), dict) else {}
        context = dict(manifest_data.get("context", {}))
        process_evidence = manifest_data.get("process_evidence") if isinstance(manifest_data.get("process_evidence"), dict) else None
        credential_type = manifest_data.get("credential_type") or issuer.get("credential_type")
        if credential_type:
            context.setdefault("credential_type", credential_type)

        if "actor_id" in manifest_data:
            actor_id = manifest_data.get("actor_id", "unknown")
            issuer_id = manifest_data.get("issuer_id")
            action = manifest_data.get("action")
            resource = manifest_data.get("resource")
            if action is None and isinstance(assertion, dict):
                action = assertion.get("action")
            if resource is None and isinstance(assertion, dict):
                resource = assertion.get("resource")
        else:
            actor_id = actor.get("entity_id", "unknown")
            issuer_id = issuer.get("issuer_id")
            action = assertion.get("action")
            resource = assertion.get("resource")

        assertions: list[dict[str, Any]] = []
        if assertion:
            assertions.append({"label": "cawg.assertion", "data": assertion})
        assertions.extend(manifest_data.get("assertions", []))

        return ManifestSignal(
            actor_id=actor_id,
            issuer_id=issuer_id,
            credential_type=credential_type,
            assertions=assertions,
            provenance_chain=manifest_data.get("provenance_chain", []),
            integrity_status=manifest_data.get("integrity_status", "verified" if manifest_data.get("integrity_ok") else "unknown"),
            action=action,
            resource=resource,
            context=context,
            process_evidence=process_evidence,
            parser_mode="fixture",
            raw_manifest=manifest_data,
        )

    @staticmethod
    def _extract_c2pa_manifest(manifest_data: dict[str, Any]) -> ManifestSignal:
        store = manifest_data.get("manifest_store", {})
        manifests = store.get("manifests", {})
        active_manifest_id = store.get("active_manifest")
        active_manifest = manifests.get(active_manifest_id, {}) if active_manifest_id else {}

        actor_id = "unknown"
        issuer_id = None
        credential_type = None
        action = None
        resource = None
        context: dict[str, Any] = {}
        assertions: list[dict[str, Any]] = []
        provenance_chain: list[str] = []
        process_evidence: dict[str, Any] | None = None

        signature_info = active_manifest.get("signature_info", {})
        if isinstance(signature_info, dict):
            issuer_id = signature_info.get("issuer") or signature_info.get("signer")

        for assertion_entry in active_manifest.get("assertions", []):
            if not isinstance(assertion_entry, dict):
                continue
            label = assertion_entry.get("label", "unlabeled")
            data = assertion_entry.get("data", {})
            assertions.append({"label": label, "data": data})

            if label in {"cawg.actions", "cawg.identity", "org.contentauthorship.identity"} and isinstance(data, dict):
                actor = data.get("actor", {}) if isinstance(data.get("actor"), dict) else {}
                actor_id = actor.get("id") or actor.get("entity_id") or data.get("actor_id") or actor_id
                issuer_id = data.get("issuer_id") or issuer_id
                credential_type = data.get("credential_type") or credential_type
                action = data.get("action") or action
                resource = data.get("resource") or resource
                for key in ["jurisdiction", "risk_tier", "content_type", "credential_type"]:
                    if key in data:
                        context[key] = data[key]

            if label == "c2pa.actions" and isinstance(data, dict) and action is None:
                actions = data.get("actions", [])
                if actions and isinstance(actions[0], dict):
                    action = actions[0].get("action") or action
                    resource = actions[0].get("resource") or resource

            if (label in PROCESS_ASSERTION_LABELS or "process" in label) and isinstance(data, dict):
                process_evidence = dict(data)
                context.setdefault("process_type", data.get("process_type", "unspecified"))

        for ingredient in active_manifest.get("ingredients", []):
            if isinstance(ingredient, dict):
                title = ingredient.get("title") or ingredient.get("instance_id") or ingredient.get("document_id")
                if title:
                    provenance_chain.append(title)

        for parent in active_manifest.get("parent_claims", []):
            if isinstance(parent, dict):
                parent_id = parent.get("manifest") or parent.get("claim") or parent.get("title")
                if parent_id:
                    provenance_chain.append(parent_id)

        if credential_type:
            context.setdefault("credential_type", credential_type)

        integrity_status = active_manifest.get("integrity_status") or manifest_data.get("integrity_status") or "verified"

        return ManifestSignal(
            actor_id=actor_id,
            issuer_id=issuer_id,
            credential_type=credential_type,
            assertions=assertions,
            provenance_chain=provenance_chain,
            integrity_status=integrity_status,
            action=action,
            resource=resource,
            context=context,
            process_evidence=process_evidence,
            parser_mode="c2pa_json",
            raw_manifest=manifest_data,
        )

    @staticmethod
    def validate_fixture(fixture_path: str | Path) -> dict[str, Any]:
        signal = CAWGManifestParser.parse_file(fixture_path)
        return {
            "valid": signal.actor_id != "unknown" and bool(signal.action) and bool(signal.resource),
            "parser_mode": signal.parser_mode,
            "has_issuer_id": signal.issuer_id is not None,
            "has_assertions": len(signal.assertions) > 0,
            "has_credential_type": signal.credential_type is not None,
            "has_process_evidence": signal.process_evidence is not None,
        }
