#!/usr/bin/env python3
"""validate-ba-planning.py — validate the ba-planning artefact JSON against the output contract.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violation list on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["T1_approach", "T2_stakeholders", "T3_governance", "T4_information_mgmt", "T5_performance"]


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be an object"]
    for key in REQUIRED:
        if key not in obj:
            errs.append(f"missing required field: {key}")
        elif obj[key] is None or obj[key] == "":
            errs.append(f"required field is empty: {key}")
    return errs


OK = {"T1_approach": {"plan_driven_pct": 70, "change_driven_pct": 30, "approver": "amaia@acme.com"}, "T2_stakeholders": [{"name": "Amaia Ruiz", "role": "VP Product", "category": "sponsor", "approver": "amaia@acme.com"}, {"name": "Bruno Lima", "role": "Eng Lead", "category": "implementer", "approver": "amaia@acme.com"}, {"name": "Carla S\u00e1", "role": "Compliance", "category": "regulator", "approver": "amaia@acme.com"}], "T3_governance": {"decision_rights": "Amaia signs scope; Bruno signs technical feasibility", "escalation_path": "Amaia \u2192 CEO@acme.com", "approver": "amaia@acme.com"}, "T4_information_mgmt": {"repo_path": "acme/ba-artefacts/initiative-x/", "retention_policy": "5y", "access_list": ["amaia@acme.com", "bruno@acme.com"]}, "T5_performance": {"metrics": ["rework_rate", "defect_density", "elicitation_throughput"], "baseline_status": "null-first-cycle"}}
BAD = {"T1_approach": "Hybrid", "T2_stakeholders": []}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: valid fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
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
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
