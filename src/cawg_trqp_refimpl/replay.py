from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .gateway import TrustGateway
from .models import VerificationRequest
from .mock_service import MockTRQPService
from .verifier import Verifier


@dataclass
class ReplayReport:
    replayed_result: dict[str, Any]
    expected_result: dict[str, Any]
    matches: bool
    differences: list[str] = field(default_factory=list)


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
    policy_path: str,
    revocation_path: str | None = None,
) -> ReplayReport:
    inputs = bundle.get("replay_inputs", {})
    request = VerificationRequest(**inputs["request"])
    profile = inputs.get("profile", "standard")
    use_gateway = bool(inputs.get("use_gateway", False))

    service = None if profile == "edge" else MockTRQPService(policy_path, revocation_path)
    gateway = TrustGateway(service) if use_gateway and service is not None else None
    verifier = Verifier(service=service, gateway=gateway)
    result = verifier.verify(request, profile=profile).to_dict()
    expected = bundle.get("verification_result", {})

    differences: list[str] = []
    for field in COMPARE_FIELDS:
        if result.get(field) != expected.get(field):
            differences.append(f"{field}: expected={expected.get(field)!r} actual={result.get(field)!r}")

    expected_epoch = inputs.get("policy_epoch")
    actual_epoch = result.get("policy_evidence", {}).get("policy_epoch")
    if expected_epoch != actual_epoch:
        differences.append(f"policy_epoch: expected={expected_epoch!r} actual={actual_epoch!r}")

    return ReplayReport(
        replayed_result=result,
        expected_result=expected,
        matches=not differences,
        differences=differences,
    )
