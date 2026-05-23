#!/usr/bin/env python3
"""validate-azure-devops-boards.py

Validate an ADO Boards config YAML/JSON against the schema in
content/02-output-contract.xml. Stdlib-only (YAML accepted only when it is
JSON-compatible; pass --json-only to force).

Inputs:
    --file PATH    path to ADO Boards config (JSON; or YAML when convertible)
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

ALLOWED_TEMPLATES = {"Basic", "Agile", "Scrum", "CMMI"}
ALLOWED_CADENCE = {"weekly", "biweekly", "monthly"}
ACTIVE_STATES = {"Active", "Doing", "In Progress", "Committed"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("organization", "project", "process_template", "area_tree",
              "iteration_tree", "board", "pat_scope_manifest"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    if obj["process_template"] not in ALLOWED_TEMPLATES:
        errs.append(f"process_template invalid: {obj['process_template']!r}")
    it = obj["iteration_tree"]
    if it.get("cadence") not in ALLOWED_CADENCE:
        errs.append(f"iteration_tree.cadence invalid: {it.get('cadence')!r}")
    if not it.get("iterations"):
        errs.append("iteration_tree.iterations empty")

    at = obj["area_tree"]
    children = set(at.get("children") or [])
    iters = set(it.get("iterations") or [])
    overlap = children & iters
    if overlap:
        errs.append(f"area_tree.children overlap iteration_tree.iterations: {sorted(overlap)}")

    board = obj["board"]
    cols = board.get("columns") or []
    if len(cols) < 3:
        errs.append("board.columns needs >=3 entries")
    for c in cols:
        state_map = set(c.get("state_mapping") or [])
        if state_map & ACTIVE_STATES and c.get("wip_limit") in (None, 0):
            errs.append(f"board column {c.get('name')!r} maps Active without wip_limit")
    if not board.get("swimlanes"):
        errs.append("board.swimlanes empty")

    pat = obj["pat_scope_manifest"]
    if not pat.get("work_items_read_write") or not pat.get("full_access_forbidden"):
        errs.append("pat_scope_manifest must have work_items_read_write=true AND full_access_forbidden=true")
    return errs


GOOD = {
    "organization": "acme", "project": "platform", "process_template": "Agile",
    "area_tree": {"root": "platform", "children": ["payments", "identity"]},
    "iteration_tree": {"cadence": "biweekly", "iterations": ["s1", "s2"]},
    "board": {
        "columns": [
            {"name": "New", "state_mapping": ["New"], "wip_limit": None},
            {"name": "Active", "state_mapping": ["Active"], "wip_limit": 5},
            {"name": "Closed", "state_mapping": ["Closed"], "wip_limit": None},
        ],
        "swimlanes": ["Default"],
    },
    "pat_scope_manifest": {"work_items_read_write": True, "full_access_forbidden": True},
}
BAD = {
    "organization": "x", "project": "y", "process_template": "Custom",
    "area_tree": {"root": "x", "children": ["s1"]},
    "iteration_tree": {"cadence": "ad-hoc", "iterations": ["s1"]},
    "board": {"columns": [{"name": "Active", "state_mapping": ["Active"]}], "swimlanes": []},
    "pat_scope_manifest": {"work_items_read_write": True, "full_access_forbidden": False},
}


def self_test() -> int:
    if validate(GOOD):
        sys.stderr.write("good rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main() -> int:
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
    text = p.read_text()
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        sys.stderr.write("pass a JSON file (YAML not supported in stdlib-only validator)\n")
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
