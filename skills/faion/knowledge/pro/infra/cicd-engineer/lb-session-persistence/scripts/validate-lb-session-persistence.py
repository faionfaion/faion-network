#!/usr/bin/env python3
"""validate-lb-session-persistence.py

Validate the session-persistence artefact against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
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

REQUIRED = ["method", "session_storage", "autoscaling", "nat_behind_lb"]
METHODS = {
    "externalized-no-sticky",
    "lb-inserted-cookie",
    "app-managed-cookie",
    "ip-hash",
    "ssl-session-id",
}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("method") not in METHODS:
        errs.append(f"method must be one of {sorted(METHODS)}")
    if obj.get("method") == "ip-hash" and (obj.get("autoscaling") or obj.get("nat_behind_lb")):
        errs.append("ip-hash forbidden with autoscaling or NAT")
    if obj.get("method") != "externalized-no-sticky":
        ttl = obj.get("sticky_ttl_seconds", 0)
        if ttl < 60:
            errs.append("sticky_ttl_seconds must be >= 60 for any sticky method")
        if obj.get("invalidate_on_removal") is not True:
            errs.append("invalidate_on_removal must be true for any sticky method")
    return errs


OK = {
    "method": "lb-inserted-cookie",
    "session_storage": "in-process",
    "autoscaling": True,
    "nat_behind_lb": True,
    "sticky_ttl_seconds": 3600,
    "invalidate_on_removal": True,
}
BAD = {
    "method": "ip-hash",
    "session_storage": "in-process",
    "autoscaling": True,
    "nat_behind_lb": True,
    "sticky_ttl_seconds": 0,
    "invalidate_on_removal": False,
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
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
