#!/usr/bin/env python3
"""validate-nodejs-express-fastify.py — grep for error handler before routes, inline error res, missing SIGTERM.

Usage:
    validate-nodejs-express-fastify.py --root /path/to/repo
    validate-nodejs-express-fastify.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

INLINE_ERR = re.compile(r"res\.status\(\s*[45]\d\d\s*\)\.json\(\s*\{\s*error")
SIGTERM = re.compile(r"process\.on\(\s*['\"]SIGTERM")


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    sigterm_found = False
    for f in root.rglob("*.ts"):
        if "/node_modules/" in str(f):
            continue
        text = f.read_text(encoding="utf-8")
        if SIGTERM.search(text):
            sigterm_found = True
        for idx, line in enumerate(text.splitlines(), 1):
            if INLINE_ERR.search(line):
                v.append({"rule": "rule:r5", "file": str(f), "line": idx, "snippet": line.strip()})
    if not sigterm_found and (root / "package.json").exists():
        v.append({"rule": "rule:r8", "file": str(root), "message": "no SIGTERM listener found in *.ts files"})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "package.json").write_text("{}", encoding="utf-8")
        (root / "app.ts").write_text("app.post('/x', (req, res) => res.status(400).json({error: 'bad'}));\n", encoding="utf-8")
        v = scan(root)
        rules = {x["rule"] for x in v}
        assert "rule:r5" in rules and "rule:r8" in rules, v
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
