from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

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
) -> ReplayReport:
    inputs = bundle.get("replay_inputs", {})
    request = VerificationRequest(**inputs["request"])
    profile_ref = inputs.get("profile", "standard")
    resolved_profile = load_profile(profile_ref)
    use_gateway = bool(inputs.get("use_gateway", False))
    policy_feed = inputs.get("policy_feed", {})
    resolved_policy_path = policy_path or policy_feed.get("policy_source")
    resolved_revocation_path = revocation_path or policy_feed.get("revocation_source")

    if resolved_profile.base_profile != "edge" and not resolved_policy_path:
        raise ValueError("policy_path is required unless replay_inputs.policy_feed.policy_source is present")

    if use_gateway:
        service = MockTRQPService(resolved_policy_path, resolved_revocation_path, transport_mode='http', transport_integrity='tls')
        gateway = TrustGateway(service)
    else:
        service = None if resolved_profile.base_profile == "edge" else MockTRQPService(resolved_policy_path, resolved_revocation_path)
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
            "policy_source": resolved_policy_path or "",
            "revocation_source": resolved_revocation_path or "",
        },
    )
