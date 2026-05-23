#!/usr/bin/env python3
"""validate-caching-strategy.py

Validate the caching-strategy artefact against the schema declared in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (OK + BAD)
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ('strategy_id', 'pattern', 'ttl_seconds_base', 'ttl_jitter_pct', 'invalidation', 'single_flight', 'hit_rate_target')


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("ttl_jitter_pct", 0) < 5:
        errs.append("ttl_jitter_pct must be >= 5 (ttl-with-jitter)")
    inv = obj.get("invalidation") or {}
    if inv.get("mode") not in {"ttl-only", "write-through", "pubsub-event"}:
        errs.append("invalidation.mode must be in {ttl-only, write-through, pubsub-event} (invalidation-contract)")
    if obj.get("single_flight") is not True:
        errs.append("single_flight must be true (single-flight-on-miss)")
    return errs


def _load_smoke():
    p = Path(__file__).resolve().parent.parent / "templates" / "_smoke-test.json"
    obj = json.loads(p.read_text())
    obj.pop("__faion_header__", None)
    return obj


def self_test() -> int:
    ok = _load_smoke()
    errs_ok = validate(ok)
    if errs_ok:
        sys.stderr.write(f"OK fixture rejected: {errs_ok}\n")
        return 1
    bad = {}
    if not validate(bad):
        sys.stderr.write("empty BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"cannot parse JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
