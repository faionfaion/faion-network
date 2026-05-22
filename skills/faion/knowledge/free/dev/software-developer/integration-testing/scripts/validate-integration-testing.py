#!/usr/bin/env python3
"""validate-integration-testing.py — check for pinned image tags + tx rollback fixture + tests/unit & tests/integration split.

Usage:
    validate-integration-testing.py --root /path/to/repo
    validate-integration-testing.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

UNPINNED = re.compile(r'(Container|image)\s*\(\s*["\']([a-z0-9-]+):latest["\']')
TX_ROLLBACK = re.compile(r"\.rollback\s*\(\)")


def scan(root: Path) -> list[dict]:
    v: list[dict] = []
    tests = root / "tests"
    if (tests / "integration").is_dir() and not (tests / "unit").is_dir():
        v.append({"rule": "rule:r4", "file": str(tests), "message": "tests/integration exists but tests/unit missing"})
    found_rollback = False
    for f in (tests / "integration").rglob("conftest.py") if (tests / "integration").is_dir() else []:
        text = f.read_text(encoding="utf-8")
        if TX_ROLLBACK.search(text):
            found_rollback = True
        for idx, line in enumerate(text.splitlines(), 1):
            m = UNPINNED.search(line)
            if m:
                v.append({"rule": "rule:r3", "file": str(f), "line": idx, "snippet": line.strip()})
    if (tests / "integration").is_dir() and not found_rollback:
        v.append({"rule": "rule:r2", "file": str(tests / "integration"), "message": "no .rollback() call found in any conftest"})
    return v


def self_test() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "tests/integration").mkdir(parents=True)
        (root / "tests/integration/conftest.py").write_text(
            'from testcontainers.postgres import PostgresContainer\n'
            'def f():\n    with PostgresContainer("postgres:latest"): pass\n',
            encoding="utf-8",
        )
        v = scan(root)
        assert any(x["rule"] == "rule:r3" for x in v), f"should flag :latest: {v}"
        assert any(x["rule"] == "rule:r4" for x in v), f"should flag missing tests/unit: {v}"
        assert any(x["rule"] == "rule:r2" for x in v), f"should flag missing rollback: {v}"
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
