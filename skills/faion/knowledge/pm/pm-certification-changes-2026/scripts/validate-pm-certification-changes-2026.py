#!/usr/bin/env python3
"""validate-pm-certification-changes-2026.py

Validate a report artefact for PM Certification Changes 2026 against the schema in
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

REQUIRED = ['effective_date', 'weights_table', 'question_type_changes', 'prep_time_deltas', 'sources']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("effective_date") != "2026-07-01":
        errs.append(f"effective_date must be '2026-07-01', got {obj.get('effective_date')!r}")
    wt = obj.get("weights_table") or []
    if not isinstance(wt, list) or len(wt) != 3:
        errs.append("weights_table must have exactly 3 rows")
    else:
        for i, row in enumerate(wt):
            for k in ("domain", "eco_2021_pct", "eco_2026_pct", "delta_pp"):
                if k not in row:
                    errs.append(f"weights_table[{i}].{k} missing")
            a = row.get("eco_2021_pct"); b = row.get("eco_2026_pct"); d = row.get("delta_pp")
            if all(isinstance(x, (int, float)) for x in (a, b, d)):
                if abs((b - a) - d) > 0.5:
                    errs.append(f"weights_table[{i}].delta_pp inconsistent")
    ptd = obj.get("prep_time_deltas") or {}
    for k in ("early_career", "mid_career", "returning"):
        if k not in ptd:
            errs.append(f"prep_time_deltas.{k} missing")
    if not obj.get("sources"):
        errs.append("sources empty")

    return errs


GOOD = {'effective_date': '2026-07-01', 'weights_table': [{'domain': 'People', 'eco_2021_pct': 42, 'eco_2026_pct': 33, 'delta_pp': -9}, {'domain': 'Process', 'eco_2021_pct': 50, 'eco_2026_pct': 41, 'delta_pp': -9}, {'domain': 'Business Environment', 'eco_2021_pct': 8, 'eco_2026_pct': 26, 'delta_pp': 18}], 'question_type_changes': ['multi-correct'], 'prep_time_deltas': {'early_career': {'extra_hours': 25, 'rationale': 'BE new'}, 'mid_career': {'extra_hours': 15, 'rationale': 'BE refresh'}, 'returning': {'extra_hours': 30, 'rationale': 'catch up'}}, 'sources': ['PMI ECO 2026 PDF']}
BAD = {'effective_date': '2026', 'weights_table': [], 'question_type_changes': [], 'prep_time_deltas': {}, 'sources': []}


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
