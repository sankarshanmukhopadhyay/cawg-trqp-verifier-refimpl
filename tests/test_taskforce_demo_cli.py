"""Verify portable taskforce report on every supported Python runtime."""
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_machine_readable_demo(tmp_path):
    output=tmp_path/"report.json"
    subprocess.run([sys.executable,str(ROOT/"scripts/run_taskforce_five_world_demo.py"),
                    "--output",str(output)],cwd=ROOT,check=True)
    report=json.loads(output.read_text(encoding="utf-8"))
    assert report["all_match"] is True
    assert report["independent_crypto_verification"] is False
    assert report["independent_interoperability"] is False
    assert len(report["results"])==5
    for entry in report["results"]:
        assert entry["matches"] is True
        assert entry["actual"]["assured_authority"]=="indeterminate"
        assert entry["actual"]["assured_coverage"]=="unverified"
        assert entry["actual"]["evidence_provenance"]["signing_time"]=="caller_supplied_untrusted"
    # Byte-identical replay proves the public output contract is deterministic.
    second=subprocess.check_output([sys.executable,str(ROOT/"scripts/run_taskforce_five_world_demo.py")],cwd=ROOT)
    assert output.read_bytes()==second
