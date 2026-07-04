from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "release-assets" / "checksums-v0.16.0.json"
TARGETS = [
    "conformance/compatibility-matrix.json",
    "conformance/risk-to-test-map.yaml",
    "conformance/assurance-suite-manifest.json",
    "examples/reproducibility_bundle_standard.json",
    "examples/exported_audit_bundle.json",
    "examples/exported_audit_bundle.signed.json",
    "examples/photography_contest/replay_bundle.json",
]


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
        "release": "v0.16.0",
        "algorithm": "sha256",
        "assets": assets,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate release asset checksums")
    parser.add_argument("--check", action="store_true", help="Check that committed checksums are current")
    args = parser.parse_args()
    manifest = build_manifest()
    content = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if args.check:
        existing = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if existing != content:
            raise SystemExit("release checksum manifest is not current")
        print("release checksum manifest is current")
        return
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
