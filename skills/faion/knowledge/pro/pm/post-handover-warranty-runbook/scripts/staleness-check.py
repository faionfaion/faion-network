#!/usr/bin/env python3
"""staleness-check.py

Flag warranty runbooks whose `last_reviewed` exceeds the published window.

Inputs:
    --file PATH       runbook frontmatter YAML / JSON
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = fresh
    1 = stale
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

FIXTURE_OK = {"owner": "x", "version": "1.0.0", "last_reviewed": "2026-05-15",
              "window_days": 30}
FIXTURE_BAD = {"owner": "x", "version": "1.0.0", "last_reviewed": "2025-12-01",
               "window_days": 30}


def check(meta: dict) -> str | None:
    last = datetime.strptime(meta["last_reviewed"], "%Y-%m-%d").date()
    window = meta.get("window_days", 30)
    age = (date.today() - last).days
    if age > window:
        return f"stale: {age}d > {window}d window"
    return None


def self_test() -> int:
    if check({**FIXTURE_OK, "last_reviewed": date.today().isoformat()}):
        sys.stderr.write("self-test FAIL: OK flagged\n")
        return 1
    if not check(FIXTURE_BAD):
        sys.stderr.write("self-test FAIL: BAD clean\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    meta = json.loads(p.read_text())
    result = check(meta)
    if result:
        sys.stdout.write(f"FINDING: {result}\n")
        return 1
    sys.stdout.write("OK fresh\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
