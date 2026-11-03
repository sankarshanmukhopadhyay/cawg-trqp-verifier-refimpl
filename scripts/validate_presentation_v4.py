#!/usr/bin/env python3
"""Validate the pinned v4 PDF and its published Pages/discovery contracts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "assets/presentations/manifest-v4.json").read_text(encoding="utf-8"))
assert manifest["artifact_version"] == "v4"
assert manifest["implementation_version"] == "v0.20.0"
assert manifest["status"] == "non-normative"
assert manifest["page_count"] == 20
assert manifest["authority"]["normative"] is False
pdf_path = ROOT / manifest["path"]
assert pdf_path.is_file(), f"Missing v4 PDF: {manifest['path']}"
pdf = pdf_path.read_bytes()
assert pdf.startswith(b"%PDF-"), "v4 asset must have PDF magic"
actual = hashlib.sha256(pdf).hexdigest()
assert actual == manifest["sha256"], f"v4 PDF digest mismatch: {actual}"
assert manifest["predecessor"]["path"] == "assets/presentations/cawg-trqp-explainer-v3.pdf"
assert (ROOT / manifest["predecessor"]["path"]).is_file(), "historical v3 PDF missing"
page = (ROOT / "docs/presentation-v4.md").read_text(encoding="utf-8")
old_page = (ROOT / "docs/presentation.md").read_text(encoding="utf-8")
home = (ROOT / "docs/index.md").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert "cawg-trqp-explainer-v4.pdf" in page
assert "presentation.md" in page and "v0.19.2" in page
assert "cawg-trqp-explainer-v3.pdf" in old_page
assert "presentation-v4.md" in home and "presentation-v4.md" in readme
print("presentation v4: PASS (v0.20.0, SHA-256 verified, v3 retained)")
