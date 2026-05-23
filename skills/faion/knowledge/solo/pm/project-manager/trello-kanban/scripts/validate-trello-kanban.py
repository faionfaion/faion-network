#!/usr/bin/env python3
"""validate-trello-kanban.py

Validate the board configuration artefact against the JSON Schema in
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
import sys
from pathlib import Path

REQUIRED = ["board_id", "lists", "labels", "rate_limit_per_10s", "ids_cached"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    lists = obj.get("lists")
    if isinstance(lists, list):
        n = len(lists)
        if n < 5 or n > 7:
            errs.append("lists count must be 5..7 (got " + str(n) + ")")
        for i, l in enumerate(lists):
            if not isinstance(l, dict) or "id" not in l or "name" not in l:
                errs.append(f"lists[{i}] missing id or name")
    elif "lists" in obj:
        errs.append("lists must be array")
    labels = obj.get("labels")
    if isinstance(labels, list):
        n = len(labels)
        if n < 1 or n > 12:
            errs.append("labels count must be 1..12 (got " + str(n) + ")")
        for i, l in enumerate(labels):
            if not isinstance(l, dict):
                continue
            if l.get("kind") not in ("type", "priority", "modifier"):
                errs.append(f"labels[{i}].kind must be in [type, priority, modifier]")
    elif "labels" in obj:
        errs.append("labels must be array")
    rl = obj.get("rate_limit_per_10s")
    if rl is not None and (not isinstance(rl, int) or rl < 1 or rl > 100):
        errs.append("rate_limit_per_10s must be 1..100")
    if obj.get("ids_cached") is not True:
        errs.append("ids_cached must be true")
    return errs


OK = {
    "board_id": "abc123",
    "lists": [
        {"id": "l1", "name": "Backlog", "wip_limit": None},
        {"id": "l2", "name": "Ready", "wip_limit": None},
        {"id": "l3", "name": "In Dev (WIP: 3)", "wip_limit": 3},
        {"id": "l4", "name": "Review (WIP: 2)", "wip_limit": 2},
        {"id": "l5", "name": "QA (WIP: 2)", "wip_limit": 2},
        {"id": "l6", "name": "Done", "wip_limit": None},
    ],
    "labels": [
        {"id": "lb1", "name": "Feature", "kind": "type"},
        {"id": "lb2", "name": "Bug", "kind": "type"},
        {"id": "lb3", "name": "P1-High", "kind": "priority"},
        {"id": "lb4", "name": "Blocked", "kind": "modifier"},
    ],
    "custom_fields": {"story_points": True, "sprint": True, "component": True},
    "butler_rules_documented_in": "constitution.md",
    "rate_limit_per_10s": 100,
    "ids_cached": True,
}
BAD = {
    "board_id": "abc",
    "lists": [
        {"id": "l1", "name": "L1"}, {"id": "l2", "name": "L2"}, {"id": "l3", "name": "L3"},
        {"id": "l4", "name": "L4"}, {"id": "l5", "name": "L5"}, {"id": "l6", "name": "L6"},
        {"id": "l7", "name": "L7"}, {"id": "l8", "name": "L8"}, {"id": "l9", "name": "L9"},
    ],
    "labels": [],
    "rate_limit_per_10s": 500,
    "ids_cached": False,
}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
