#!/usr/bin/env python3
"""validate-go-error-handling.py — check Go source for %v wrap, type-assert, leaked driver errors.

Usage:
    validate-go-error-handling.py --root /path/to/repo
    validate-go-error-handling.py --self-test

Inputs:
    --root PATH   Go repo
Outputs: stdout JSON {ok, violations}
Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PCT_V_WRAP = re.compile(r'fmt\.Errorf\([^)]*%v[^)]*,\s*\w+\)')
TYPE_ASSERT_ERR = re.compile(r'\w+\s*,\s*ok\s*:=\s*\w+\.\(\*?AppError\)')
DRIVER_IN_HANDLER = re.compile(r'\b(pgx\.ErrNoRows|sql\.ErrNoRows|redis\.Nil)\b')


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    for f in root.rglob("*.go"):
        if "/vendor/" in str(f):
            continue
        text = f.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), 1):
            if PCT_V_WRAP.search(line):
                v.append({"rule": "rule:r2", "file": str(f), "line": idx, "snippet": line.strip()})
            if TYPE_ASSERT_ERR.search(line):
                v.append({"rule": "rule:r2", "file": str(f), "line": idx, "snippet": line.strip(),
                          "note": "use errors.As, not type assertion"})
            if DRIVER_IN_HANDLER.search(line) and ("/handler/" in str(f) or "/handlers/" in str(f)):
                v.append({"rule": "rule:r3", "file": str(f), "line": idx, "snippet": line.strip(),
                          "note": "driver error leaked to handler"})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "internal/handler").mkdir(parents=True)
        (root / "internal/handler/user.go").write_text(
            'package handler\nimport "github.com/jackc/pgx/v5"\n'
            'func H() { if err := f(); err == pgx.ErrNoRows { return } }\n',
            encoding="utf-8"
        )
        v = scan(root)
        assert any("rule:r3" in x["rule"] for x in v), f"should flag driver leak: {v}"
        (root / "x.go").write_text('package x\nfunc F(err error) error { return fmt.Errorf("bad: %v", err) }\n', encoding="utf-8")
        v = scan(root)
        assert any("rule:r2" in x["rule"] for x in v), f"should flag %v wrap: {v}"
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
