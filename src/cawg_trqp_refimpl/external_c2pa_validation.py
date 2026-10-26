"""Fail-closed, opt-in adapter to the external c2patool validator.

This produces an independently executed C2PA tool receipt, NOT CAWG delegation
conformance. It never treats manifest presence as trusted signer identity.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

MAX_REPORT_BYTES = 4 * 1024 * 1024

def validate_c2pa_asset(asset_path: str | Path, *, executable: str = "c2patool",
                        timeout_seconds: int = 30) -> dict:
    path = Path(asset_path).resolve(strict=True)
    if not path.is_file():
        raise ValueError("asset_not_file")
    asset_sha256 = hashlib.sha256(path.read_bytes()).hexdigest()
    receipt = {"adapter": "c2patool-cli-v1", "asset_sha256": asset_sha256,
               "manifest_integrity": "indeterminate", "signer_trust": "not_evaluated",
               "delegated_authority": "not_evaluated", "trusted_signing_time": "not_evaluated",
               "tool_exit_code": None, "validation_codes": []}
    if not 1 <= timeout_seconds <= 120:
        raise ValueError("timeout_out_of_bounds")
    if not executable or "/" in executable or "\\" in executable:
        raise ValueError("executable_must_be_path_lookup_name")
    try:
        run = subprocess.run([executable, str(path)], shell=False,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             timeout=timeout_seconds, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        receipt["reason"] = "validator_unavailable"
        return receipt
    receipt["tool_exit_code"] = run.returncode
    if len(run.stdout) > MAX_REPORT_BYTES or len(run.stderr) > MAX_REPORT_BYTES:
        receipt["reason"] = "validator_output_too_large"
        return receipt
    try:
        report = json.loads(run.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        receipt["reason"] = "validator_output_invalid"
        return receipt
    if not isinstance(report, dict):
        receipt["reason"] = "validator_report_malformed"
        return receipt
    statuses = report.get("validation_status")
    if statuses is None:
        receipt["reason"] = "validation_status_absent"
        return receipt
    if not isinstance(statuses, list) or any(not isinstance(s, dict) or not isinstance(s.get("code"), str) for s in statuses):
        receipt["reason"] = "validation_status_malformed"
        return receipt
    receipt["validation_codes"] = sorted({s["code"] for s in statuses})
    if run.returncode != 0 or statuses:
        receipt["manifest_integrity"] = "failed"
        receipt["reason"] = "reported_validation_failure"
        return receipt
    if not isinstance(report.get("active_manifest"), str) or not report["active_manifest"]:
        receipt["reason"] = "active_manifest_absent"
        return receipt
    receipt["manifest_integrity"] = "validated_by_external_tool"
    receipt["reason"] = "local_c2pa_validation_completed"
    return receipt
