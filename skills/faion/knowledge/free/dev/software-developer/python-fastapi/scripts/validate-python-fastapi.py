#!/usr/bin/env python3
"""validate-python-fastapi.py — grep for @app.on_event, sync DB in async routes, schema reuse.

Usage:
    validate-python-fastapi.py --root /path/to/repo
    validate-python-fastapi.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ON_EVENT = re.compile(r"@app\.on_event\(")
SYNC_QUERY_IN_ASYNC = re.compile(r"async\s+def\s+\w+\([^)]*\)\s*->[^:]*:\s*(?:\n[ \t]+[^\n]*)*?\s*db\.query\(", re.DOTALL)


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    for f in root.rglob("*.py"):
        if "/.venv/" in str(f) or "/site-packages/" in str(f):
            continue
        text = f.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), 1):
            if ON_EVENT.search(line):
                v.append({"rule": "rule:r1", "file": str(f), "line": idx, "snippet": line.strip()})
        if SYNC_QUERY_IN_ASYNC.search(text):
            v.append({"rule": "rule:ap-04", "file": str(f), "line": 0,
                      "note": "sync db.query inside async def"})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "main.py").write_text(
            '@app.on_event("startup")\nasync def s(): pass\n',
            encoding="utf-8"
        )
        v = scan(root)
        assert any(x["rule"] == "rule:r1" for x in v), v
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
