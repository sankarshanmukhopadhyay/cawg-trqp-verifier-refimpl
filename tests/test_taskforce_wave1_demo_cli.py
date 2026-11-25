"""Reproduce the public demonstration through the documented entry point."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_wave1_cli_deterministic_and_non_elevating(tmp_path):
    args = [sys.executable, str(ROOT / "scripts/run_taskforce_wave1_demo.py")]
    a = subprocess.run(args, cwd=ROOT, capture_output=True, check=True).stdout
    b = subprocess.run(args, cwd=ROOT, capture_output=True, check=True).stdout
    assert a == b
    report = json.loads(a)
    assert report["all_match"]
    assert report["independent_interoperability"] is False
    assert len(report["results"]) == 6
    for row in report["results"]:
        assert row["actual"]["assured_authority"] == "indeterminate"
        assert row["actual"]["assured_consent"] == "indeterminate"
        assert row["wrong_actor"]["delegation_at_use"] == "signed_terms_out_of_scope"
    target = tmp_path / "report.json"
    subprocess.run(args + ["--output", str(target)], cwd=ROOT, check=True)
    assert target.read_bytes() == a
