#!/usr/bin/env python3
"""validate-pm-certification-alignment-2026.py

Validate a rubric artefact for PM Certification Alignment 2026 against the schema in
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

REQUIRED = ['analysis_date', 'methodology_count', 'coverage_by_domain', 'coverage_gaps', 'themes_covered']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    DOMAINS = {"People", "Process", "Business Environment"}
    THEMES = {"business-acumen", "data-driven", "strategic-alignment",
              "agile-hybrid", "leadership-skills"}
    cov = obj.get("coverage_by_domain") or {}
    missing = DOMAINS - set(cov.keys())
    if missing:
        errs.append(f"coverage_by_domain missing: {sorted(missing)}")
    weights = []
    for d in DOMAINS:
        entry = cov.get(d) or {}
        for k in ("count", "weight_pct"):
            if k not in entry:
                errs.append(f"coverage_by_domain.{d}.{k} missing")
        if isinstance(entry.get("weight_pct"), (int, float)):
            weights.append(entry["weight_pct"])
    if weights and abs(sum(weights) - 100) > 1:
        errs.append(f"weight_pct sum {sum(weights)} != 100")
    for i, g in enumerate(obj.get("coverage_gaps") or []):
        for k in ("gap", "owner", "due_date"):
            if k not in g:
                errs.append(f"coverage_gaps[{i}].{k} missing")
    for t in obj.get("themes_covered") or []:
        if t not in THEMES:
            errs.append(f"theme not canonical: {t!r}")
    if not isinstance(obj.get("methodology_count"), int) or obj["methodology_count"] < 1:
        errs.append("methodology_count must be >=1")

    return errs


GOOD = {'analysis_date': '2026-05-22', 'methodology_count': 130, 'coverage_by_domain': {'People': {'count': 35, 'weight_pct': 33}, 'Process': {'count': 60, 'weight_pct': 41}, 'Business Environment': {'count': 35, 'weight_pct': 26}}, 'coverage_gaps': [{'gap': 'x', 'owner': 'U', 'due_date': '2026-09-30'}], 'themes_covered': ['business-acumen', 'data-driven', 'strategic-alignment', 'agile-hybrid', 'leadership-skills']}
BAD = {'analysis_date': 'y', 'methodology_count': 0, 'coverage_by_domain': {'People': {}}, 'coverage_gaps': [{'gap': 'x'}], 'themes_covered': ['random']}


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
