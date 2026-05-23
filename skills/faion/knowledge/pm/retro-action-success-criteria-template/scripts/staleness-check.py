#!/usr/bin/env python3
"""staleness-check.py

Flag methodology artefact whose header.last_reviewed exceeds the 90-day window.
Stdlib-only.

Inputs:
    --file PATH       path to artefact JSON
    --window-days N   default 90
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = fresh
    1 = stale
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def is_stale(obj: dict, window_days: int) -> bool:
    lr = obj.get("header", {}).get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
    except Exception:
        return True
    return (dt.date.today() - d).days > window_days


def self_test() -> int:
    fresh = {"header": {"last_reviewed": dt.date.today().isoformat()}}
    stale = {"header": {"last_reviewed": "2020-01-01"}}
    if is_stale(fresh, 90):
        sys.stderr.write("fresh marked stale\n"); return 1
    if not is_stale(stale, 90):
        sys.stderr.write("stale marked fresh\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--window-days", type=int, default=90)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    if is_stale(obj, args.window_days):
        sys.stderr.write(f"STALE: last_reviewed exceeds {args.window_days} days\n")
        return 1
    sys.stdout.write("FRESH\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
