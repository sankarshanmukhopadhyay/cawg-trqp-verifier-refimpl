from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = ROOT / "pyproject.toml"
TARGETS = [
    "conformance/compatibility-matrix.json",
    "conformance/risk-to-test-map.yaml",
    "conformance/assurance-suite-manifest.json",
    "portfolio/integration-contract.json",
    "examples/reproducibility_bundle_standard.json",
    "examples/exported_audit_bundle.json",
    "examples/exported_audit_bundle.signed.json",
    "examples/photography_contest/replay_bundle.json",
]


def _release() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, flags=re.MULTILINE)
    if not match:
        raise SystemExit("unable to resolve release version from pyproject.toml")
    return f"v{match.group(1)}"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_manifest() -> dict:
    assets = []
    for target in TARGETS:
        path = ROOT / target
        assets.append({
            "path": target,
            "sha256": _sha256(path),
            "bytes": path.stat().st_size,
        })
    return {
        "release": _release(),
        "algorithm": "sha256",
        "assets": assets,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate release asset checksums")
    parser.add_argument("--check", action="store_true", help="Check that committed checksums are current")
    args = parser.parse_args()
    release = _release()
    output = ROOT / "release-assets" / f"checksums-{release}.json"
    manifest = build_manifest()
    content = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if args.check:
        existing = output.read_text(encoding="utf-8") if output.exists() else ""
        if existing != content:
            raise SystemExit(f"release checksum manifest is not current: {output.relative_to(ROOT)}")
        print(f"release checksum manifest is current: {output.relative_to(ROOT)}")
        return
    output.parent.mkdir(exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(f"wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
