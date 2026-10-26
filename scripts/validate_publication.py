#!/usr/bin/env python3
"""Check public release/state consistency without relying on network availability."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []

def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

def require(ok, message):
    if not ok:
        errors.append(message)

pyproject = read("pyproject.toml")
m = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.M)
require(bool(m), "package version missing")
version = m.group(1) if m else "unknown"
tag = "v" + version
readme = read("README.md")
require("**Latest published release:** " + tag in readme, "README latest-release identity drift")
require((ROOT / ("RELEASE_NOTES_" + tag + ".md")).is_file(), "release notes missing")
require('current_version: "' + version + '"' in read("data/repository-metadata.yaml"), "metadata release drift")
require('version: "' + version + '"' in read("CITATION.cff"), "citation release drift")
require(tag in read("ROADMAP.md"), "roadmap release drift")
for path in ("conformance/compatibility-matrix.json", "conformance/assurance-suite-manifest.json"):
    require(json.loads(read(path)).get("release") == tag, path + ": release mismatch")
contract = json.loads(read("portfolio/integration-contract.json"))
require(contract["repository"]["version"] == version, "portfolio version mismatch")
for path in contract["local_evidence"]:
    require((ROOT / path).is_file(), "local evidence missing: " + path)
asset = contract.get("published_release_evidence", {})
require(asset.get("tag") == tag, "remote release-asset identity mismatch")
require(asset.get("checksum_asset", "").endswith("/" + tag + "/checksums-" + tag + ".json"), "release checksum-asset reference mismatch")
changelog = read("CHANGELOG.md")
require(changelog.startswith("---\n"), "changelog front matter must start at byte zero")
require(changelog.count("## [Unreleased]") == 1, "changelog must have exactly one active Unreleased heading")
for item in ("0.19.1", version):
    require("## [" + item + "]" in changelog, "changelog missing " + item)
for path in ("CHANGELOG.md", "QUICKSTART.md", "GOVERNANCE.md", "ROADMAP.md", "SECURITY.md", "CONTRIBUTING.md"):
    require(read(path).startswith("---\n"), "root Jekyll page lacks leading front matter: " + path)
require("post-v0.19.2" in readme, "README omits post-release development boundary")
require("experimental" in read("docs/external-c2pa-validation-boundary.md").lower(), "external validation experimental status missing")
if errors:
    for error in errors:
        print("publication: FAIL: " + error)
    sys.exit(1)
print("publication: PASS (" + tag + ")")
