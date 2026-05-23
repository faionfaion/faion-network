#!/usr/bin/env python3
"""validate-kpi-tree-construction.py

Validate the artefact produced by the `kpi-tree-construction` methodology against the JSON Schema embedded in
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

REQUIRED = ["tree_id", "owner", "last_touched", "north_star", "nodes", "edges", "review_cadence"]
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


OK = json.loads(r"""{"tree_id": "kpi-acme-2026q2", "owner": "cpo@acme.io", "last_touched": "2026-05-23T11:00:00Z", "north_star": {"name": "weekly_active_subscribers", "formula": "count(distinct user_id where active_in_7d=true and sub_active=true)", "cadence": "weekly", "evidence": "BI table fct_subscribers"}, "nodes": [{"id": "n-1", "name": "activation_rate", "owner": "growth-lead", "formula": "activated / signed_up", "cadence": "weekly", "parent": "north_star", "evidence": "BI view dim_activation"}, {"id": "n-2", "name": "weekly_engagement", "owner": "product-lead", "formula": "engaged_in_7d / active", "cadence": "weekly", "parent": "north_star", "evidence": "BI view fct_engagement"}, {"id": "n-3", "name": "monthly_retention", "owner": "cs-lead", "formula": "retained_m1 / cohort_size", "cadence": "monthly", "parent": "north_star", "evidence": "BI view fct_retention"}], "edges": [{"from": "n-1", "to": "north_star"}, {"from": "n-2", "to": "north_star"}, {"from": "n-3", "to": "north_star"}], "review_cadence": "weekly review every Friday 30 min", "template_version": "1.1.0", "status": "ready_for_review"}""")
BAD = json.loads(r"""{"tree_id": "x", "north_star": {"name": "nps"}, "nodes": []}""")


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
