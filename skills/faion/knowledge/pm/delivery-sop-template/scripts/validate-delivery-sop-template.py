#!/usr/bin/env python3
"""validate-delivery-sop-template.py

Validate a spec artefact for Service Delivery SOP Template against the schema in
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

REQUIRED = ['sop_id', 'service_name', 'version', 'owner', 'steps', 'engagement_acceptance']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    import re
    if not re.match(r"^[0-9]+\.[0-9]+\.[0-9]+$", str(obj.get("version", ""))):
        errs.append(f"version pattern invalid: {obj.get('version')!r}")
    steps = obj.get("steps") or []
    if not isinstance(steps, list) or not (5 <= len(steps) <= 15):
        errs.append(f"steps count {len(steps)} outside 5..15")
    else:
        for i, st in enumerate(steps):
            for k in ("n", "name", "inputs", "action", "decisions",
                      "quality_gates", "escalation", "time_budget_min"):
                if k not in st:
                    errs.append(f"steps[{i}].{k} missing")
            if isinstance(st.get("quality_gates"), list) and not st["quality_gates"]:
                errs.append(f"steps[{i}].quality_gates empty")
    if not obj.get("engagement_acceptance"):
        errs.append("engagement_acceptance empty")

    return errs


GOOD = {'sop_id': 'sop-1', 'service_name': 'analytics', 'version': '1.0.0', 'owner': 'U_F', 'steps': [{'n': 1, 'name': 's1', 'inputs': ['x'], 'action': 'do', 'decisions': [], 'quality_gates': ['check'], 'escalation': 'U_F', 'time_budget_min': 30}, {'n': 2, 'name': 's2', 'inputs': ['x'], 'action': 'do', 'decisions': [], 'quality_gates': ['check'], 'escalation': 'U_F', 'time_budget_min': 30}, {'n': 3, 'name': 's3', 'inputs': ['x'], 'action': 'do', 'decisions': [], 'quality_gates': ['check'], 'escalation': 'U_F', 'time_budget_min': 30}, {'n': 4, 'name': 's4', 'inputs': ['x'], 'action': 'do', 'decisions': [], 'quality_gates': ['check'], 'escalation': 'U_F', 'time_budget_min': 30}, {'n': 5, 'name': 's5', 'inputs': ['x'], 'action': 'do', 'decisions': [], 'quality_gates': ['check'], 'escalation': 'U_F', 'time_budget_min': 30}], 'engagement_acceptance': ['client signs']}
BAD = {'sop_id': 'x', 'service_name': 'y', 'version': '1.0', 'owner': 'z', 'steps': [{'n': 1, 'name': 'do'}], 'engagement_acceptance': []}


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
