from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .jsoncanon import sha256_hex
from .gateway import TrustGateway
from .models import VerificationRequest
from .mock_service import MockTRQPService
from .profile import load_profile
from .verifier import Verifier


@dataclass
class ReplayReport:
    replayed_result: dict[str, Any]
    expected_result: dict[str, Any]
    matches: bool
    differences: list[str] = field(default_factory=list)
    policy_sources: dict[str, str] = field(default_factory=dict)


COMPARE_FIELDS = (
    "asset_integrity",
    "assertion_binding",
    "issuer_recognition",
    "actor_authorization",
    "process_integrity",
    "policy_freshness",
    "verification_mode",
    "trust_outcome",
)



def replay_audit_bundle(
    bundle: dict[str, Any],
    *,
    policy_path: str | None = None,
    revocation_path: str | None = None,
    trusted_root: str | Path = ".",
) -> ReplayReport:
    inputs = bundle.get("replay_inputs", {})
    request = VerificationRequest(**inputs["request"])
    profile_ref = inputs.get("profile", "standard")
    resolved_profile = load_profile(profile_ref)
    use_gateway = bool(inputs.get("use_gateway", False))
    policy_feed = inputs.get("policy_feed", {})
    root = Path(trusted_root).resolve()
    resolved_policy_path = _verified_bundle_path(
        policy_path or policy_feed.get("policy_source"),
        policy_feed.get("policy_source_sha256") if policy_path is None else None,
        root,
        "policy_source",
    )
    resolved_revocation_path = _verified_bundle_path(
        revocation_path or policy_feed.get("revocation_source"),
        policy_feed.get("revocation_source_sha256") if revocation_path is None else None,
        root,
        "revocation_source",
        required=False,
    )
    policy_descriptor_path = _verified_bundle_path(
        policy_feed.get("policy_descriptor_source"),
        policy_feed.get("policy_descriptor_source_sha256"),
        root,
        "policy_descriptor_source",
        required=False,
    )
    revocation_descriptor_path = _verified_bundle_path(
        policy_feed.get("revocation_descriptor_source"),
        policy_feed.get("revocation_descriptor_source_sha256"),
        root,
        "revocation_descriptor_source",
        required=False,
    )
    trust_anchors_path = _verified_bundle_path(
        policy_feed.get("trust_anchors_source", "data/trust_anchors.json"),
        policy_feed.get("trust_anchors_source_sha256"),
        root,
        "trust_anchors_source",
        required=False,
    )

    if resolved_profile.base_profile != "edge" and not resolved_policy_path:
        raise ValueError("policy_path is required unless replay_inputs.policy_feed.policy_source is present")

    if use_gateway:
        service = MockTRQPService(
            resolved_policy_path,
            resolved_revocation_path,
            transport_mode='http',
            transport_integrity='tls',
            policy_descriptor_path=policy_descriptor_path,
            revocation_descriptor_path=revocation_descriptor_path,
            trust_anchors_path=trust_anchors_path,
        )
        gateway = TrustGateway(service)
    else:
        service = None if resolved_profile.base_profile == "edge" else MockTRQPService(
            resolved_policy_path,
            resolved_revocation_path,
            policy_descriptor_path=policy_descriptor_path,
            revocation_descriptor_path=revocation_descriptor_path,
            trust_anchors_path=trust_anchors_path,
        )
        gateway = None
    verifier = Verifier(service=service, gateway=gateway)
    result = verifier.verify(request, profile=resolved_profile).to_dict()
    expected = bundle.get("verification_result", {})

    differences: list[str] = []
    for field in COMPARE_FIELDS:
        if result.get(field) != expected.get(field):
            differences.append(f"{field}: expected={expected.get(field)!r} actual={result.get(field)!r}")

    expected_epoch = inputs.get("policy_epoch")
    actual_epoch = result.get("policy_evidence", {}).get("policy_epoch")
    if expected_epoch != actual_epoch:
        differences.append(f"policy_epoch: expected={expected_epoch!r} actual={actual_epoch!r}")

    expected_profile = inputs.get("profile")
    actual_profile = result.get("policy_evidence", {}).get("verification_profile")
    if isinstance(expected_profile, dict) and actual_profile != expected_profile:
        differences.append("verification_profile: expected bundle replay_inputs.profile to match replayed policy_evidence.verification_profile")

    expected_transport = inputs.get('transport_metadata')
    actual_transport = result.get('policy_evidence', {}).get('transport')
    if expected_transport and actual_transport != expected_transport:
        differences.append('transport_metadata: expected replay_inputs.transport_metadata to match replayed policy_evidence.transport')

    expected_revocation = inputs.get('revocation_status')
    actual_revocation = result.get('policy_evidence', {}).get('revocation_status')
    if expected_revocation and actual_revocation != expected_revocation:
        differences.append('revocation_status: expected replay_inputs.revocation_status to match replayed policy_evidence.revocation_status')

    return ReplayReport(
        replayed_result=result,
        expected_result=expected,
        matches=not differences,
        differences=differences,
        policy_sources={
            "policy_source": _display_replay_path(resolved_policy_path, root),
            "revocation_source": _display_replay_path(resolved_revocation_path, root),
        },
    )


def _verified_bundle_path(
    path_value: str | None,
    expected_digest: str | None,
    trusted_root: Path,
    label: str,
    *,
    required: bool = True,
) -> str | None:
    if not path_value:
        if required:
            raise ValueError(f"{label} is required for replay")
        return None
    path = Path(path_value)
    resolved = path.resolve() if path.is_absolute() else (trusted_root / path).resolve()
    try:
        resolved.relative_to(trusted_root)
    except ValueError as exc:
        raise ValueError(f"{label} must resolve under trusted replay root {trusted_root}") from exc
    if not resolved.exists():
        if required:
            raise ValueError(f"{label} does not exist: {path_value}")
        return None
    if expected_digest:
        actual = sha256_hex(resolved.read_text(encoding="utf-8"))
        if actual != expected_digest:
            raise ValueError(f"{label} digest mismatch")
    return str(resolved)


def _display_replay_path(path_value: str | None, trusted_root: Path) -> str:
    if not path_value:
        return ""
    path = Path(path_value).resolve()
    try:
        return str(path.relative_to(trusted_root))
    except ValueError:
        return str(path)
