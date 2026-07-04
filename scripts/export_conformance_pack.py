from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ROOT = ROOT / "fixtures" / "profile-bound"
OUTPUT = ROOT / "conformance" / "assurance-suite-manifest.json"


def _fixture_entry(path: Path) -> dict:
    manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
    assurance_level = {
        "standard": "AL2",
        "high_assurance": "AL4",
        "edge": "AL2",
    }.get(manifest["profile"], "AL1")
    return {
        "fixture_id": manifest["fixture_id"],
        "profile": manifest["profile"],
        "assurance_level": assurance_level,
        "verification_mode": manifest["verification_mode"],
        "vector_class": "positive",
        "implementation_identity": "cawg-trqp-refimpl",
        "inputs": manifest["inputs"],
        "replay_contract": manifest["replay_contract"],
        "fixture_path": str(path.relative_to(ROOT)),
    }


def build_manifest() -> dict:
    fixtures = [_fixture_entry(path) for path in sorted(FIXTURE_ROOT.iterdir()) if path.is_dir()]
    return {
        "schema_version": "2026-07-03",
        "release": "v0.16.0",
        "implementation_identity": {
            "id": "cawg-trqp-refimpl",
            "role": "reference_implementation",
            "authority_scope": "CAWG manifest verification using TRQP-governed trust decisions",
        },
        "evidence_artifacts": [
            "verification_result",
            "decision_receipt",
            "audit_bundle",
            "replay_bundle",
            "feed_descriptor_evidence",
        ],
        "fixtures": fixtures,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export the external assurance-suite manifest")
    parser.add_argument("--check", action="store_true", help="Check that the committed manifest is current")
    args = parser.parse_args()
    manifest = build_manifest()
    content = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    if args.check:
        existing = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if existing != content:
            raise SystemExit("conformance/assurance-suite-manifest.json is not current")
        print("assurance-suite manifest is current")
        return
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
