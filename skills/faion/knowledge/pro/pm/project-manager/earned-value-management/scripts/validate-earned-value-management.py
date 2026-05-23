#!/usr/bin/env python3
"""validate-earned-value-management.py

Validate a report artefact for Earned Value Management against the schema in
content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    path to artefact JSON
    --self-test    run built-in fixtures and exit
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['project_id', 'period', 'pv', 'ev', 'ac', 'cpi', 'spi', 'eac', 'eac_method', 'status_color']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    import re
    if not re.match(r"^[0-9]{4}-[0-9]{2}$", str(obj.get("period", ""))):
        errs.append(f"period pattern invalid: {obj.get('period')!r}")
    if obj.get("eac_method") not in {"BAC_over_CPI", "AC_plus_ETC", "optimistic", "regression"}:
        errs.append(f"eac_method invalid: {obj.get('eac_method')!r}")
    if obj.get("status_color") not in {"green", "amber", "red"}:
        errs.append(f"status_color invalid: {obj.get('status_color')!r}")
    cpi = obj.get("cpi"); spi = obj.get("spi"); sc = obj.get("status_color")
    if isinstance(cpi, (int, float)) and isinstance(spi, (int, float)):
        if cpi >= 0.95 and spi >= 0.95 and sc != "green":
            errs.append("color/index mismatch: both indices green but color != green")
        if (cpi < 0.85 or spi < 0.85) and sc != "red":
            errs.append("color/index mismatch: index < 0.85 but color != red")
    if obj.get("status_color") == "red" and not obj.get("corrective_action_plan"):
        errs.append("red status without corrective_action_plan")

    return errs


GOOD = {'project_id': 'acme', 'period': '2026-05', 'pv': 100000, 'ev': 95000, 'ac': 105000, 'cpi': 0.905, 'spi': 0.95, 'eac': 220000, 'eac_method': 'BAC_over_CPI', 'status_color': 'amber'}
BAD = {'project_id': 'x', 'period': 'May', 'pv': 100, 'ev': 90, 'ac': 110, 'cpi': 0.82, 'spi': 0.9, 'eac': 250, 'eac_method': 'guess', 'status_color': 'yellow'}


def self_test():
    if validate(GOOD):
        sys.stderr.write("good rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n"); return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
