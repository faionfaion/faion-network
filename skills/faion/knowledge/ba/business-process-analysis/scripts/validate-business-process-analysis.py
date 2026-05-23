#!/usr/bin/env python3
"""validate-business-process-analysis.py

Validate a report artefact produced by the business-process-analysis methodology
against the JSON Schema captured in content/02-output-contract.xml.

stdlib-only. Inputs / outputs / exit codes documented under --help.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixture
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

REQUIRED = ['process_id', 'name', 'owner', 'tier', 'va_pct', 'bn_pct', 'nva_pct', 'baseline_metrics', 'diff_table', 'framework_anchor']


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"process_id": "P-0042", "name": "Order to Cash", "owner": "Finance Ops", "tier": "deep", "va_pct": 0.55, "bn_pct": 0.2, "nva_pct": 0.25, "baseline_metrics": {"volume_per_year": 120000, "cycle_time_minutes": 38, "cost_per_transaction": 4.2}, "diff_table": [{"step": "Credit check", "current_actor": "AR clerk", "future_actor": "S/4 automated rule", "change_type": "automate", "risk": "model drift", "dependency": "S/4 credit module"}], "framework_anchor": "APQC PCF 9.1.1", "deviation_log": [], "ownership_decision": "hybrid"}')
BAD = json.loads('{"process_id": "OTC", "name": "Order to Cash"}')


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: good fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: bad fixture accepted\n")
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
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"VIOLATION: invalid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
