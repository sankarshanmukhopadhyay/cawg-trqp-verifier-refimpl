#!/usr/bin/env python3
"""Bounded HTTP crawl of the public Pages site; writes machine-readable evidence."""
import argparse
import json
import time
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = dict(attrs).get("href")
        if href:
            self.links.append(href)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--site", default="https://sankarshanmukhopadhyay.github.io/cawg-trqp-verifier-refimpl/")
    p.add_argument("--max-pages", type=int, default=250)
    p.add_argument("--max-external", type=int, default=100)
    p.add_argument("--output", default="publication-link-audit.json")
    args = p.parse_args()
    site = args.site.rstrip("/") + "/"
    origin = urlparse(site)
    base_path = origin.path
    queue = deque([site])
    checked = set()
    external = set()
    failures = []
    status = {}
    while queue and len(checked) < args.max_pages:
        url = queue.popleft()
        if url in checked:
            continue
        checked.add(url)
        try:
            with urlopen(Request(url, headers={"User-Agent": "CAWG-TRQP-publication-audit/1.0"}), timeout=12) as resp:
                code = resp.status
                content_type = resp.headers.get("Content-Type", "")
                body = resp.read(2 * 1024 * 1024) if "text/html" in content_type else b""
            status[url] = code
            if "text/html" in content_type:
                parser = Links()
                parser.feed(body.decode("utf-8", errors="replace"))
                for href in parser.links:
                    if href.startswith(("mailto:", "tel:", "javascript:", "data:", "#")):
                        continue
                    absolute = urldefrag(urljoin(url, href)).url
                    target = urlparse(absolute)
                    if target.scheme not in ("http", "https"):
                        continue
                    if target.netloc == origin.netloc and target.path.startswith(base_path):
                        if absolute not in checked:
                            queue.append(absolute)
                    elif target.netloc:
                        external.add(absolute)
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            failures.append({"url": url, "error": str(exc)})
    # External checks are bounded and separate so transient third-party failures
    # remain independently classifiable from broken first-party Pages links.
    external_failures = []
    for url in sorted(external)[:args.max_external]:
        try:
            with urlopen(Request(url, headers={"User-Agent": "CAWG-TRQP-publication-audit/1.0"}), timeout=8) as resp:
                if resp.status >= 400:
                    external_failures.append({"url": url, "status": resp.status})
        except HTTPError as exc:
            # Rate limiting and access restrictions are not necessarily broken links.
            external_failures.append({"url": url, "status": exc.code, "classification": "restricted" if exc.code in (401, 403, 429) else "http_error"})
        except (URLError, TimeoutError, OSError, ValueError) as exc:
            external_failures.append({"url": url, "error": str(exc), "classification": "unavailable"})
    report = {"site": site, "checked_at_unix": int(time.time()), "pages_checked": len(checked),
              "internal_failures": failures, "external_discovered": len(external),
              "external_checked": min(len(external), args.max_external),
              "external_findings": external_failures, "truncated_internal": bool(queue),
              "truncated_external": len(external) > args.max_external}
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"pages_checked": report["pages_checked"], "internal_failures": len(failures),
                      "external_findings": len(external_failures)}, indent=2))
    if failures or report["truncated_internal"]:
        raise SystemExit("public Pages crawl incomplete or first-party URL failures")

if __name__ == "__main__":
    main()
