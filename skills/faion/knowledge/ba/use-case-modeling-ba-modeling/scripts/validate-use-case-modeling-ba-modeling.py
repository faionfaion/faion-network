#!/usr/bin/env python3
"""validate-use-case-modeling.py

Validate a use-case set against 02-output-contract.xml.

Inputs:
    --file PATH       path to set JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid; 1 = invalid; 2 = usage / unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER = re.compile(r"^v\d+\.\d+\.\d+$")
PRED_OP = re.compile(r"[=!<>]")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    if not SEMVER.match(obj.get("version_tag", "")):
        errs.append("version_tag must match semver pattern")
    ucs = obj.get("use_cases", [])
    if not ucs:
        errs.append("use_cases must be non-empty")
    for i, u in enumerate(ucs):
        pa = (u.get("primary_actor", "") or "").strip()
        if not pa or pa.lower() in ("user", "customer", "person") or len(pa.split()) < 2:
            errs.append(f"use_cases[{i}].primary_actor anonymous (rule r1)")
        if not (u.get("trace_id") or "").strip():
            errs.append(f"use_cases[{i}].trace_id empty (rule r5)")
        if " and " in (u.get("goal", "") or "").lower():
            errs.append(f"use_cases[{i}].goal contains 'AND' — single-goal violated (rule r4)")
        if len(u.get("main_success_scenario", [])) < 3:
            errs.append(f"use_cases[{i}].main_success_scenario must have >= 3 steps (rule r2)")
        if len(u.get("main_success_scenario", [])) > 10:
            errs.append(f"use_cases[{i}].main_success_scenario > 10 — split required (rule r4)")
        if not u.get("alternative_flows"):
            errs.append(f"use_cases[{i}].alternative_flows empty (rule r2)")
        if not u.get("exception_flows"):
            errs.append(f"use_cases[{i}].exception_flows empty (rule r2)")
        for cond in u.get("preconditions", []) + u.get("postconditions", []):
            if not PRED_OP.search(cond or ""):
                errs.append(f"use_cases[{i}] precondition/postcondition '{cond}' has no operator (rule r3)")
        if not u.get("preconditions"):
            errs.append(f"use_cases[{i}].preconditions empty (rule r3)")
        if not u.get("postconditions"):
            errs.append(f"use_cases[{i}].postconditions empty (rule r3)")
    return errs


OK_FIXTURE = {
    "set_id": "x", "version_tag": "v1.0.0",
    "use_cases": [{
        "id": "uc-1", "trace_id": "PROD-1",
        "primary_actor": "Authenticated Patient",
        "goal": "Book one appointment slot",
        "preconditions": ["session.authenticated == true"],
        "postconditions": ["appointment.status == 'booked'"],
        "main_success_scenario": ["1. select", "2. reserve", "3. confirm"],
        "alternative_flows": [{"id": "alt", "trigger": "x", "steps": ["y"]}],
        "exception_flows": [{"id": "exc", "trigger": "x", "steps": ["y"]}],
    }]
}
BAD_FIXTURE = {
    "set_id": "x", "version_tag": "v1.0.0",
    "use_cases": [{"id": "uc-1", "trace_id": "", "primary_actor": "User",
                   "goal": "Book and pay and confirm", "preconditions": ["logged in"], "postconditions": ["ok"],
                   "main_success_scenario": ["one"], "alternative_flows": [], "exception_flows": []}]
}


def self_test() -> int:
    if validate(OK_FIXTURE):
        sys.stderr.write("OK rejected\n"); return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("BAD accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
