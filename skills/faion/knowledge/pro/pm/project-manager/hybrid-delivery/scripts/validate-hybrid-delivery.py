#!/usr/bin/env python3
"""validate-hybrid-delivery.py

Validate a spec artefact for Hybrid Delivery against the schema in
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

REQUIRED = ['program_id', 'workstreams', 'handoffs', 'governance', 'reporting_dashboard']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    ws = obj.get("workstreams") or []
    if not isinstance(ws, list) or len(ws) < 2:
        errs.append("workstreams must have >=2 entries (else not hybrid)")
    else:
        for i, w in enumerate(ws):
            for k in ("id", "name", "mode", "cadence", "lead", "rationale"):
                if k not in w:
                    errs.append(f"workstreams[{i}].{k} missing")
            if w.get("mode") not in {"predictive", "agile"}:
                errs.append(f"workstreams[{i}].mode invalid: {w.get('mode')!r}")
            if isinstance(w.get("rationale"), str) and len(w["rationale"]) < 30:
                errs.append(f"workstreams[{i}].rationale too short")
    hs = obj.get("handoffs") or []
    for j, h in enumerate(hs):
        for k in ("from_ws", "to_ws", "inputs", "outputs", "acceptance_criteria",
                  "sla_days", "escalation_owner"):
            if k not in h:
                errs.append(f"handoffs[{j}].{k} missing")
    gov = obj.get("governance") or {}
    if gov.get("layer") != "single":
        errs.append("governance.layer must be 'single'")

    return errs


GOOD = {'program_id': 'acme', 'workstreams': [{'id': 'ws-1', 'name': 'hw', 'mode': 'predictive', 'cadence': 'monthly', 'lead': 'U_HW', 'rationale': 'Regulated hardware path requires predictive baseline.'}, {'id': 'ws-2', 'name': 'fw', 'mode': 'agile', 'cadence': '2w sprint', 'lead': 'U_FW', 'rationale': 'Firmware features iterate weekly with prototypes; agile fits.'}], 'handoffs': [{'from_ws': 'ws-1', 'to_ws': 'ws-2', 'inputs': ['board'], 'outputs': ['proto'], 'acceptance_criteria': ['smoke'], 'sla_days': 5, 'escalation_owner': 'U_PD'}], 'governance': {'layer': 'single', 'decision_authority': 'U_SC'}, 'reporting_dashboard': {'common_metrics': ['cv'], 'translation_rules': ['v*c']}}
BAD = {'program_id': 'x', 'workstreams': [{'id': 'ws-1', 'name': 'x', 'mode': 'hybrid'}], 'handoffs': [], 'governance': {'layer': 'dual'}, 'reporting_dashboard': {}}


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
