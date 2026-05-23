#!/usr/bin/env python3
"""validate-pm-tool-selection.py

Validate a decision-record artefact for PM Tool Selection against the schema in
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

REQUIRED = ['decision_id', 'decision_maker', 'context', 'options', 'decision', 'consequences', 'reversal_trigger']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    import re
    if not re.match(r"^ADR-[0-9]{4}$", str(obj.get("decision_id", ""))):
        errs.append(f"decision_id pattern invalid: {obj.get('decision_id')!r}")
    if not obj.get("decision_maker") or obj["decision_maker"].lower() == "committee":
        errs.append(f"decision_maker invalid: {obj.get('decision_maker')!r}")
    if not isinstance(obj.get("context"), str) or len(obj.get("context", "")) < 50:
        errs.append("context must be >=50 chars")
    opts = obj.get("options") or []
    if not isinstance(opts, list) or len(opts) < 3:
        errs.append(f"options count {len(opts)} < 3")
    DIMS = {"ecosystem", "governance", "integrations", "agent_api", "tco"}
    for i, o in enumerate(opts):
        sc = o.get("scorecard") or {}
        missing = DIMS - set(sc.keys())
        if missing:
            errs.append(f"options[{i}].scorecard missing: {sorted(missing)}")
    rt = obj.get("reversal_trigger") or {}
    for k in ("metric", "threshold", "rationale"):
        if k not in rt:
            errs.append(f"reversal_trigger.{k} missing")

    return errs


GOOD = {'decision_id': 'ADR-0014', 'decision_maker': 'U_HEAD', 'context': 'We have 25 PM users on Jira; switching cost acceptable; need tool with REST+agent API.', 'options': [{'vendor': 'Jira', 'scorecard': {'ecosystem': 9, 'governance': 8, 'integrations': 9, 'agent_api': 7, 'tco': 6}}, {'vendor': 'Linear', 'scorecard': {'ecosystem': 6, 'governance': 7, 'integrations': 8, 'agent_api': 9, 'tco': 8}}, {'vendor': 'ADO', 'scorecard': {'ecosystem': 8, 'governance': 9, 'integrations': 8, 'agent_api': 8, 'tco': 7}}], 'decision': 'Linear', 'consequences': ['lower TCO'], 'reversal_trigger': {'metric': 'lock-in', 'threshold': '>30% TCO', 'rationale': 'x'}}
BAD = {'decision_id': '14', 'decision_maker': '', 'context': 'x', 'options': [{'vendor': 'Jira'}], 'decision': 'Jira', 'consequences': [], 'reversal_trigger': {}}


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
