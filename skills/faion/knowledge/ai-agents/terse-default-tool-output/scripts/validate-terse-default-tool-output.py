#!/usr/bin/env python3
"""validate-terse-default-tool-output.py

Validate a tool response JSON against the terse-default envelope schema from
content/02-output-contract.xml.

Inputs:
    --file PATH       path to JSON to validate
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("format", "total_hits", "truncated"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    fmt = obj.get("format")
    if fmt not in ("summary", "full"):
        errs.append("format must be one of: summary, full")
    if not isinstance(obj.get("total_hits"), int) or obj.get("total_hits", -1) < 0:
        errs.append("total_hits must be int >= 0")
    if not isinstance(obj.get("truncated"), bool):
        errs.append("truncated must be bool")
    if fmt == "summary":
        if "table" not in obj:
            errs.append("summary mode requires 'table'")
    elif fmt == "full":
        if "rows" not in obj or not isinstance(obj["rows"], list):
            errs.append("full mode requires 'rows' (list)")
        else:
            for i, r in enumerate(obj["rows"]):
                if not isinstance(r, dict) or "id" not in r:
                    errs.append(f"rows[{i}] missing 'id'")
        reason = obj.get("reason")
        if not isinstance(reason, str) or len(reason) < 4:
            errs.append("full mode requires 'reason' (string, >= 4 chars)")
    return errs


OK_SUMMARY = {"format": "summary", "total_hits": 3, "truncated": False, "table": "| id |\n|---|\n| L-1 |"}
OK_FULL = {"format": "full", "total_hits": 1, "truncated": False, "rows": [{"id": "L-1", "msg": "x"}], "reason": "audit"}
BAD_NO_FLAGS = {"format": "summary", "table": "x"}
BAD_FULL_NO_REASON = {"format": "full", "total_hits": 1, "truncated": False, "rows": [{"id": "L-1"}]}


def self_test() -> int:
    if validate(OK_SUMMARY):
        sys.stderr.write("ok_summary rejected\n"); return 1
    if validate(OK_FULL):
        sys.stderr.write("ok_full rejected\n"); return 1
    if not validate(BAD_NO_FLAGS):
        sys.stderr.write("bad_no_flags accepted\n"); return 1
    if not validate(BAD_FULL_NO_REASON):
        sys.stderr.write("bad_full_no_reason accepted\n"); return 1
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
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
