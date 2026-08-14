#!/usr/bin/env python3
"""asset-stamp.py — content-hash static asset URLs in HTML so a CDN edge cannot
serve a stale file after a green deploy.

Assets are normally served `cache-control: immutable, max-age=31536000`, so an
edge object outlives any number of deploys. Measured on a live Cloudflare-fronted
site: hours after a successful deploy, `GET /assets/js/main.js` returned a
three-day-old 735-byte file with `cf-cache-status: HIT` and `age: 280134`, while
the origin held the current 10,487-byte file. CI was green throughout, because
nothing in a normal pipeline looks at what the edge actually serves.

Page HTML is `cf-cache-status: DYNAMIC` and never edge-cached, so the URL the
HTML emits is the one lever a build controls without CDN credentials. Appending
the file's own content hash makes a changed asset a URL the edge has never seen,
while an unchanged asset keeps its URL and stays cached. Purging by API needs
credentials; this needs none.

This tool does NOT verify what the edge serves — it cannot, it never makes a
network request. It guarantees only that the HTML you ship addresses the bytes
you built.

Input:  --dir with HTML files, --root the web root the URLs resolve against
Output: rewritten HTML in place (or a findings list under --check)

Exit: 0 every asset URL is stamped and current · 1 --check found a URL that is
      unstamped or carries a stale hash · 2 the tool could not run.
Zero model calls. Zero network calls.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

NAME = "asset-stamp"

# Only href="…" / src="…" attributes. An asset path inside a JavaScript string
# literal is deliberately NOT matched: rewriting a value the page later compares
# or keys on is how a cache fix becomes a data bug.
TAG_TEMPLATE = r'((?:href|src)=")({prefix}[^"?\s]+)(?:\?v=[0-9a-f]+)?(")'

OK_FIXTURE = '<link href="/assets/a.css"><script src="/assets/b.js?v=deadbeef01">'
BAD_FIXTURE = '<link href="/assets/missing.css">'


def digest(root: Path, url: str) -> str | None:
    """First 10 hex of sha256 over the file's bytes, or None if it is not there."""
    try:
        return hashlib.sha256(
            (root / url.lstrip("/")).read_bytes()).hexdigest()[:10]
    except OSError:
        return None


def rewrite(root: Path, text: str, prefix: str) -> tuple[str, list[str]]:
    """Stamp every asset URL. Returns the new text and one finding per URL whose
    file is missing. Idempotent: an existing `?v=` is replaced, not appended, so
    a second run is a no-op and --check stays meaningful."""
    findings: list[str] = []
    tag = re.compile(TAG_TEMPLATE.format(prefix=re.escape(prefix)))

    def sub(match: re.Match) -> str:
        url = match.group(2)
        hashed = digest(root, url)
        if hashed is None:
            findings.append(f"{url}: no such file under the web root")
            return match.group(1) + url + match.group(3)
        return f"{match.group(1)}{url}?v={hashed}{match.group(3)}"

    return tag.sub(sub, text), findings


def self_test() -> list[str]:
    """Prove the rewriter still behaves against a fixture tree it builds in memory."""
    failures: list[str] = []
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "assets").mkdir()
        (root / "assets" / "a.css").write_bytes(b"body{}")
        (root / "assets" / "b.js").write_bytes(b"void 0")

        once, findings = rewrite(root, OK_FIXTURE, "/assets/")
        if findings:
            failures.append(f"OK fixture produced findings: {findings}")
        if "?v=" not in once:
            failures.append("OK fixture was not stamped")
        twice, _ = rewrite(root, once, "/assets/")
        if twice != once:
            failures.append("rewrite is not idempotent")
        if once.count("?v=") != 2:
            failures.append(f"expected 2 stamps, got {once.count('?v=')}")

        _, bad = rewrite(root, BAD_FIXTURE, "/assets/")
        if not bad:
            failures.append("BAD fixture produced no finding")
    return failures


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", help="directory of HTML files to stamp")
    ap.add_argument("--root", help="web root the asset URLs resolve against")
    ap.add_argument("--prefix", default="/assets/",
                    help="URL prefix treated as an asset path")
    ap.add_argument("--glob", default="*.html",
                    help="which files under the directory to stamp")
    ap.add_argument("--check", action="store_true",
                    help="report drift and write nothing")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in fixtures and exit")
    args = ap.parse_args()

    if args.self_test:
        failures = self_test()
        for failure in failures:
            print(f"{NAME}: self-test: {failure}", file=sys.stderr)
        print(f"{NAME}: self-test checks=5 failures={len(failures)}")
        return 1 if failures else 0

    if not args.dir or not args.root:
        print(f"{NAME}: --dir and --root are both required", file=sys.stderr)
        return 2
    source, root = Path(args.dir), Path(args.root)
    if not source.is_dir() or not root.is_dir():
        print(f"{NAME}: --dir and --root must be directories", file=sys.stderr)
        return 2

    pages = sorted(source.rglob(args.glob))
    findings: list[str] = []
    changed = 0
    for page in pages:
        try:
            before = page.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            print(f"{NAME}: cannot read {page}: {exc}", file=sys.stderr)
            return 2
        after, missing = rewrite(root, before, args.prefix)
        findings += [f"{page}: {m}" for m in missing]
        if after == before:
            continue
        if args.check:
            findings.append(f"{page}: asset URL unstamped or stale")
        else:
            page.write_text(after, encoding="utf-8")
        changed += 1

    for finding in findings:
        print(f"{NAME}: {finding}", file=sys.stderr)
    verb = "drifted" if args.check else "stamped"
    print(f"{NAME}: pages={len(pages)} {verb}={changed} "
          f"findings={len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
