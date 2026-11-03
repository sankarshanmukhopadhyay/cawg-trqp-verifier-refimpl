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
require("post-" + tag in readme, "README omits current release development boundary")
require("experimental" in read("docs/external-c2pa-validation-boundary.md").lower(), "external validation experimental status missing")
# Guard against presenting the historical v3 deck or synthetic taskforce cases as current assured capability.
presentation = read("docs/presentation.md")
require("Historical presentation (v0.19.2 scope)" in presentation, "presentation historical scope notice missing")
require("presentation-v4.md" in presentation, "historic v3 page does not link to v4")
require((ROOT / "docs/presentation-v4.md").is_file(), "v4 presentation landing page missing")
require("presentation-v4.md" in read("docs/index.md"), "home page does not expose v4 presentation")
require("v0.20.0" in presentation, "presentation lacks link to newer experimental baseline")
demo = read("docs/agentic-ai/taskforce-five-world-demo.md")
require("v0.20.0" in demo, "experimental demonstration release reference missing")
require("No new release or normative version is implied." not in demo, "stale pre-release demonstration statement")
agentic = read("docs/agentic-ai/index.md")
require("tests/test_enterprise_binding_assurance.py" in agentic, "agentic adoption path omits authority assurance tests")
readiness = read("docs/release-readiness.md")
require("python scripts/generate_release_checksums.py\npython scripts/generate_release_checksums.py --check" in readiness,
        "release readiness checksum reproduction commands require generation before check")
require("python scripts/generate_release_checksums.py\npython scripts/generate_release_checksums.py --check" in readme,
        "README checksum reproduction commands require generation before check")
if errors:
    for error in errors:
        print("publication: FAIL: " + error)
    sys.exit(1)
print("publication: PASS (" + tag + ")")
