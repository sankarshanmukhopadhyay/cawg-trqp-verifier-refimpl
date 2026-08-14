"""Semantic assurance controls for CAWG/C2PA assertion expectations and conflicts.

The controls in this module are intentionally relying-party policy controls. They do
not redefine CAWG or C2PA normative semantics. They make missing, unsupported, and
conflicting evidence observable so that a verifier cannot silently collapse those
states into a generic success result.
"""
from __future__ import annotations

from typing import Any


def _assertions(request_context: dict[str, Any]) -> list[dict[str, Any]]:
    value = request_context.get("_manifest_assertions", [])
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def evaluate_assertions(context: dict[str, Any], controls: dict[str, Any]) -> tuple[dict[str, Any], list[str], bool, bool]:
    assertions = _assertions(context)
    labels = [str(item.get("label", "unlabeled")) for item in assertions]
    present = sorted(set(labels))
    required = list(controls.get("required_labels", []))
    supported = set(controls.get("supported_labels", []))
    missing = sorted(label for label in required if label not in present)
    unsupported = sorted(label for label in required if label in present and supported and label not in supported)
    unknown = sorted(label for label in present if supported and label not in supported)

    reasons: list[str] = []
    blocking = False
    degraded = False
    if missing:
        enforcement = controls.get("missing_required", "observe")
        reasons.append(f"Missing required assertions: {', '.join(missing)}")
        blocking |= enforcement == "fail"
        degraded |= enforcement == "warn"
    if unsupported:
        enforcement = controls.get("unsupported_required", "observe")
        reasons.append(f"Required assertions are present but unsupported: {', '.join(unsupported)}")
        blocking |= enforcement == "fail"
        degraded |= enforcement == "warn"
    if unknown:
        enforcement = controls.get("unknown_assertion", "preserve")
        if enforcement in {"warn", "fail"}:
            reasons.append(f"Unknown or unsupported assertion labels observed: {', '.join(unknown)}")
        blocking |= enforcement == "fail"
        degraded |= enforcement == "warn"

    status = "verified"
    if blocking:
        status = "failed"
    elif degraded:
        status = "warning"
    elif missing or unsupported:
        status = "observed_gap"
    elif not assertions:
        status = "not_evaluated" if required else "not_applicable"

    report = {
        "status": status,
        "expected": required,
        "present": present,
        "missing": missing,
        "unsupported": unsupported,
        "unknown": unknown,
        "unknown_assertion_policy": controls.get("unknown_assertion", "preserve"),
    }
    return report, reasons, blocking, degraded


def _read_path(data: Any, path: str) -> Any:
    current = data
    for part in path.split(".") if path else []:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def evaluate_conflicts(context: dict[str, Any], controls: dict[str, Any]) -> tuple[dict[str, Any], list[str], bool, bool]:
    assertions = _assertions(context)
    findings: list[dict[str, Any]] = []
    reasons: list[str] = []
    enforcement = controls.get("enforcement", "observe")

    for rule in controls.get("rules", []):
        labels = list(rule.get("labels", []))
        claim_path = str(rule.get("claim_path", ""))
        observations = []
        for item in assertions:
            label = item.get("label")
            if label not in labels:
                continue
            value = _read_path(item.get("data", {}), claim_path)
            if value is not None:
                observations.append({"label": label, "value": value})
        distinct = {repr(obs["value"]) for obs in observations}
        if len(distinct) <= 1:
            continue

        strategy = rule.get("strategy", "unresolved")
        resolved = False
        selected = None
        if strategy == "precedence":
            for preferred in rule.get("precedence", labels):
                selected = next((obs for obs in observations if obs["label"] == preferred), None)
                if selected is not None:
                    resolved = True
                    break
        finding = {
            "rule_id": rule.get("id", "unnamed-conflict-rule"),
            "claim_path": claim_path,
            "observations": observations,
            "status": "resolved" if resolved else "conflicted",
            "selected": selected,
        }
        findings.append(finding)
        reasons.append(f"Conflicting assertions detected by {finding['rule_id']} at {claim_path}")

    unresolved = [item for item in findings if item["status"] == "conflicted"]
    blocking = bool(unresolved) and enforcement == "fail"
    degraded = bool(unresolved) and enforcement == "warn"
    report = {
        "status": "conflicted" if unresolved else ("resolved" if findings else "not_applicable"),
        "enforcement": enforcement,
        "findings": findings,
    }
    return report, reasons, blocking, degraded
