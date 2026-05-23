#!/usr/bin/env python3
"""validate-change-control.py

Validate a spec artefact for Change Control against the schema in
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

REQUIRED = ['project_id', 'baseline_version', 'change_requests']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    crs = obj.get("change_requests") or []
    if not isinstance(crs, list):
        errs.append("change_requests must be list")
    else:
        for i, cr in enumerate(crs):
            for k in ("id", "requester", "submitted_at", "status", "tier",
                      "impact_analysis"):
                if k not in cr:
                    errs.append(f"change_requests[{i}].{k} missing")
            if cr.get("status") == "approved" and not cr.get("decision_record"):
                errs.append(f"change_requests[{i}] approved without decision_record")
            ia = cr.get("impact_analysis") or {}
            for k in ("cost_delta_pct", "schedule_delta_days", "scope_delta", "risk_delta"):
                if k not in ia:
                    errs.append(f"change_requests[{i}].impact_analysis.{k} missing")

    return errs


GOOD = {'project_id': 'acme', 'baseline_version': 'v1', 'change_requests': [{'id': 'CR-0001', 'requester': 'U_PO', 'submitted_at': '2026-05-20T10:00:00Z', 'status': 'approved', 'tier': 'tier-2', 'impact_analysis': {'cost_delta_pct': 4.5, 'schedule_delta_days': 7, 'scope_delta': 'add billing retry', 'risk_delta': 'decreases'}, 'decision_record': {'approver': 'U_S', 'decided_at': '2026-05-22T15:00:00Z', 'rationale': 'value > cost'}}]}
BAD = {'project_id': 'x', 'baseline_version': '', 'change_requests': [{'id': '42', 'requester': 'x', 'submitted_at': 'now', 'status': 'ok', 'tier': 'small'}]}


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
