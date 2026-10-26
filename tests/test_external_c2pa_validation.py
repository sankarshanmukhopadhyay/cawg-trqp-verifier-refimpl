"""Offline, deterministic tests of the c2patool invocation trust boundary."""
import json
import subprocess
from types import SimpleNamespace
from unittest.mock import patch
from pathlib import Path
from cawg_trqp_refimpl.external_c2pa_validation import validate_c2pa_asset

def asset(tmp_path):
    p=tmp_path/"test-image.jpg"
    p.write_bytes(b"offline test data; not a real C2PA asset")
    return p

def mock_output(report, exit_code=0):
    return SimpleNamespace(returncode=exit_code, stdout=json.dumps(report).encode(), stderr=b"")

def test_success_is_limited_to_manifest_integrity(tmp_path):
    p=asset(tmp_path)
    with patch("cawg_trqp_refimpl.external_c2pa_validation.subprocess.run",return_value=mock_output({"active_manifest":"urn:manifest","validation_status":[]})) as invoked:
        r=validate_c2pa_asset(p)
    assert invoked.call_args.kwargs["shell"] is False
    assert invoked.call_args.args[0]==["c2patool",str(p.resolve())]
    assert r["manifest_integrity"]=="validated_by_external_tool"
    assert r["signer_trust"]=="not_evaluated"
    assert r["delegated_authority"]=="not_evaluated"
    assert r["trusted_signing_time"]=="not_evaluated"

def test_fails_closed_on_validation_errors(tmp_path):
    with patch("cawg_trqp_refimpl.external_c2pa_validation.subprocess.run",return_value=mock_output({"active_manifest":"urn:manifest","validation_status":[{"code":"claimSignature.mismatch"}]})):
        r=validate_c2pa_asset(asset(tmp_path))
    assert r["manifest_integrity"]=="failed"
    assert r["validation_codes"]==["claimSignature.mismatch"]

def test_nonzero_exit_fails_closed(tmp_path):
    with patch("cawg_trqp_refimpl.external_c2pa_validation.subprocess.run",return_value=mock_output({"active_manifest":"urn:manifest","validation_status":[]},3)):
        assert validate_c2pa_asset(asset(tmp_path))["manifest_integrity"]=="failed"

def test_missing_or_malformed_status_stays_indeterminate(tmp_path):
    for report in ({"active_manifest":"urn:manifest"},{"active_manifest":"urn:manifest","validation_status":"bad"},
                   {"validation_status":[]},{"active_manifest":"urn:manifest","validation_status":[{"bad":"code"}]}):
        with patch("cawg_trqp_refimpl.external_c2pa_validation.subprocess.run",return_value=mock_output(report)):
            assert validate_c2pa_asset(asset(tmp_path))["manifest_integrity"]=="indeterminate"

def test_timeout_or_tool_missing_stays_indeterminate(tmp_path):
    for error in (FileNotFoundError(),subprocess.TimeoutExpired("c2patool",1)):
        with patch("cawg_trqp_refimpl.external_c2pa_validation.subprocess.run",side_effect=error):
            assert validate_c2pa_asset(asset(tmp_path))["reason"]=="validator_unavailable"

def test_command_not_shell_or_external_fetch(tmp_path):
    p=asset(tmp_path)
    for name in ("../c2patool","/usr/bin/c2patool",""):
        try:
            validate_c2pa_asset(p,executable=name)
        except ValueError:
            continue
        assert False, name
