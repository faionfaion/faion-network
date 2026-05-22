#!/usr/bin/env python3
"""validate-mobile-responsive.py — grep CSS for fixed px widths, 100vh, desktop-first media queries.

Usage:
    validate-mobile-responsive.py --root /path/to/repo
    validate-mobile-responsive.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

WIDTH_PX = re.compile(r"width\s*:\s*([0-9]+)px")
VH100 = re.compile(r"\b100vh\b")
DESKTOP_FIRST = re.compile(r"@media\s*\(\s*max-width\b")


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    for f in root.rglob("*.css"):
        if "/node_modules/" in str(f):
            continue
        for idx, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for m in WIDTH_PX.finditer(line):
                if int(m.group(1)) > 1:
                    v.append({"rule": "rule:r3", "file": str(f), "line": idx, "snippet": line.strip()})
            if VH100.search(line):
                v.append({"rule": "rule:r5", "file": str(f), "line": idx, "snippet": line.strip()})
            if DESKTOP_FIRST.search(line):
                v.append({"rule": "rule:r2", "file": str(f), "line": idx, "snippet": line.strip()})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "a.css").write_text("@media (max-width: 768px) { .x { width: 360px; height: 100vh; } }\n", encoding="utf-8")
        v = scan(root)
        rules = {x["rule"] for x in v}
        assert "rule:r2" in rules and "rule:r3" in rules and "rule:r5" in rules
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.root:
        ap.error("--root required")
        return 2
    v = scan(args.root)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
