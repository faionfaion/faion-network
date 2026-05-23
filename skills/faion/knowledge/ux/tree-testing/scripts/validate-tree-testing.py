#!/usr/bin/env python3
"""validate-tree-testing.py

Validate the artefact for the tree-testing methodology against the schema in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
PRIORITIES = {'critical', 'medium', 'low', 'high'}
METRICS = {'success_rate', 'directness', 'first_click', 'time'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'tree-testing':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'config':
            errs.append("__faion_header__.produces mismatch")
    if 'tree' not in obj:
        errs.append(f"missing required field: " + 'tree')
    if 'tasks' not in obj:
        errs.append(f"missing required field: " + 'tasks')
    if 'sample_plan' not in obj:
        errs.append(f"missing required field: " + 'sample_plan')
    if 'metrics' not in obj:
        errs.append(f"missing required field: " + 'metrics')


    tr = obj.get("tree") or {}
    nodes = tr.get("nodes") or []
    if not isinstance(nodes, list) or len(nodes) < 5:
        errs.append("tree.nodes must have >=5 entries")
    depth = tr.get("depth")
    if not isinstance(depth, int) or depth < 1 or depth > 4:
        errs.append("tree.depth must be in 1-4")
    tasks = obj.get("tasks") or []
    if len(tasks) < 3 or len(tasks) > 8:
        errs.append("tasks count must be in 3-8")
    for i, t in enumerate(tasks):
        if t.get("priority") not in PRIORITIES:
            errs.append("tasks[" + str(i) + "].priority invalid")
    sp = obj.get("sample_plan") or {}
    n = sp.get("n_per_arm")
    if not isinstance(n, int) or n < 30:
        errs.append("sample_plan.n_per_arm must be >=30")
    arms = sp.get("arms") or []
    if not isinstance(arms, list) or not arms:
        errs.append("sample_plan.arms must be non-empty list")
    m = obj.get("metrics") or []
    if "directness" not in m:
        errs.append("metrics must include 'directness'")

    return errs


OK = {'__faion_header__': {'methodology': 'tree-testing', 'version': '1.1.0', 'produces': 'config'}, 'tree': {'nodes': ['home', 'products', 'products/billing', 'products/billing/invoice', 'support', 'docs'], 'depth': 3}, 'tasks': [{'id': 't1', 'prompt': "Where would you go to download last month's invoice?", 'expected_target': 'products/billing/invoice', 'priority': 'critical'}, {'id': 't2', 'prompt': 'Where would you go for setup help?', 'expected_target': 'support', 'priority': 'high'}, {'id': 't3', 'prompt': 'Where would you go for API docs?', 'expected_target': 'docs', 'priority': 'medium'}], 'sample_plan': {'n_per_arm': 50, 'arms': ['variant-A']}, 'metrics': ['success_rate', 'directness', 'first_click']}
BAD = {'tree': {'nodes': ['a', 'b'], 'depth': 6}, 'tasks': [], 'sample_plan': {'n_per_arm': 12, 'arms': []}, 'metrics': ['success_rate']}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
