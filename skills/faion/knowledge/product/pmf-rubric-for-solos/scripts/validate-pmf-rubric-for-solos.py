#!/usr/bin/env python3
"""validate-pmf-rubric-for-solos.py

Validate the artefact produced by the `pmf-rubric-for-solos` methodology against the JSON Schema embedded in
`content/02-output-contract.xml`. Stdlib-only.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["rubric_id", "owner", "last_touched", "dimensions", "scores", "verdict", "thresholds"]
PLACEHOLDERS = {"TBD", "TODO", "FIXME"}


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
            continue
        v = obj[k]
        if v in (None, "", [], {}):
            errs.append(f"required field empty: {k}")
        if isinstance(v, str) and v.strip().upper() in PLACEHOLDERS:
            errs.append(f"placeholder value in field: {k}")
    owner = obj.get("owner")
    if isinstance(owner, str) and owner.lower().strip() in {"team", "we", "tbd"}:
        errs.append("owner must be a single named person, not 'team' / 'we' / 'TBD'")
    return errs


OK = json.loads(r"""{"rubric_id": "pmf-jane-2026q2", "owner": "jane@indie.io", "last_touched": "2026-05-23T11:00:00Z", "dimensions": ["very_disappointed_pct", "w12_retention", "organic_pull", "willingness_to_pay", "founder_confidence", "runway_fit"], "scores": {"very_disappointed_pct": 38, "w12_retention": 0.22, "organic_pull": 0.18, "willingness_to_pay": 0.11, "founder_confidence": 3, "runway_fit": 4, "evidence": "Tally survey 2026-05-22 + BI cohort 2026-05-22"}, "verdict": "near-pmf", "thresholds": {"very_disappointed_pct": 40, "w12_retention": 0.25, "organic_pull": 0.2, "willingness_to_pay": 0.1}, "template_version": "1.1.0", "status": "ready_for_review"}""")
BAD = json.loads(r"""{"rubric_id": "x", "scores": {}, "verdict": "good"}""")


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"valid fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
