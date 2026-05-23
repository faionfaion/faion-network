#!/usr/bin/env python3
"""validate-event-sourcing-snapshots.py

Validate a snapshot-policy spec against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 valid · 1 invalid · 2 usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["aggregate", "interval_events", "storage_table", "version_aware", "invalidation_on_schema_bump", "loader_fallback"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
TABLE_RE = re.compile(r"^[a-z][a-z0-9_]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "aggregate" in obj and not NAME_RE.match(str(obj["aggregate"])):
        errs.append("aggregate must be PascalCase")
    n = obj.get("interval_events")
    if not isinstance(n, int) or n < 50 or n > 100:
        errs.append("interval_events must be int in [50, 100]")
    if "storage_table" in obj and not TABLE_RE.match(str(obj["storage_table"])):
        errs.append("storage_table must be snake_case")
    if obj.get("version_aware") is not True:
        errs.append("version_aware must be true")
    if obj.get("invalidation_on_schema_bump") is not True:
        errs.append("invalidation_on_schema_bump must be true")
    if obj.get("loader_fallback") != "replay_from_zero":
        errs.append("loader_fallback must be 'replay_from_zero'")
    if obj.get("treated_as_truth") is True:
        errs.append("treated_as_truth must be false (cache-only)")
    return errs


OK = {
    "aggregate": "Wallet",
    "interval_events": 100,
    "storage_table": "wallet_snapshots",
    "version_aware": True,
    "invalidation_on_schema_bump": True,
    "loader_fallback": "replay_from_zero",
    "invalidation_script": "python -m snapshots.invalidate Wallet",
    "treated_as_truth": False,
}
BAD = {
    "aggregate": "Wallet",
    "interval_events": 5,
    "storage_table": "Snapshots",
    "version_aware": False,
    "invalidation_on_schema_bump": False,
    "loader_fallback": "crash",
    "invalidation_script": "",
    "treated_as_truth": True,
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
