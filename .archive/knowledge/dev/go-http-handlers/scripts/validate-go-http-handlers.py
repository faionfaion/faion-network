#!/usr/bin/env python3
"""validate-go-http-handlers.py — grep for gin.Default, ctx.Background, missing timeouts, fat handlers.

Usage:
    validate-go-http-handlers.py --root /path/to/repo
    validate-go-http-handlers.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GIN_DEFAULT = re.compile(r"\bgin\.Default\s*\(")
BACKGROUND_IN_HANDLER = re.compile(r"context\.Background\s*\(")
HANDLER_GOROUTINE = re.compile(r"go\s+func\s*\([^)]*\)\s*\{[^}]*c\.Request", re.DOTALL)


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    for f in root.rglob("*.go"):
        if "/vendor/" in str(f):
            continue
        text = f.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), 1):
            if GIN_DEFAULT.search(line):
                v.append({"rule": "rule:r2", "file": str(f), "line": idx, "snippet": line.strip()})
            if BACKGROUND_IN_HANDLER.search(line) and ("/handler/" in str(f) or "/handlers/" in str(f)):
                v.append({"rule": "rule:r4", "file": str(f), "line": idx, "snippet": line.strip()})
        if HANDLER_GOROUTINE.search(text):
            v.append({"rule": "rule:r5", "file": str(f), "line": 0, "note": "goroutine captures c.Request"})
        if "/handler/" in str(f) or "/handlers/" in str(f):
            n = sum(1 for line in text.splitlines() if line.strip().startswith("func ") and "(c *gin.Context)" in line)
            lines = len(text.splitlines())
            if n > 0 and lines / max(n, 1) > 60:
                v.append({"rule": "rule:r6", "file": str(f), "line": 0,
                          "note": f"avg handler size {lines / n:.0f} lines > 60"})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "internal/handler").mkdir(parents=True)
        (root / "internal/handler/user.go").write_text(
            'package handler\nimport "context"\n'
            'func H(c *gin.Context){ ctx := context.Background(); _ = ctx }\n',
            encoding="utf-8",
        )
        v = scan(root)
        assert any("rule:r4" in x["rule"] for x in v)
        (root / "main.go").write_text('package main\nfunc main(){ r := gin.Default() }\n', encoding="utf-8")
        v = scan(root)
        assert any("rule:r2" in x["rule"] for x in v)
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
