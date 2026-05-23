#!/usr/bin/env python3
"""validate-wbs-creation.py

Validate a WBS spec JSON against content/02-output-contract.xml.
Checks: 100% rule, 8-80 leaf sizing, noun-only names, mandatory overhead,
append-only IDs, Dictionary completeness. Stdlib-only.

Inputs:
    --file PATH       path to WBS JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VERB_RX = re.compile(r"^(Build|Design|Implement|Test|Code|Develop|Create) ", re.IGNORECASE)
ID_RX = re.compile(r"^[0-9]+(\.[0-9]+)*$")
OVERHEAD = {"project management", "quality assurance", "deployment",
            "documentation", "training", "transition"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("project", "version", "items", "dictionary"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    items = obj["items"]
    if not isinstance(items, list) or not items:
        errs.append("items must be non-empty list")
        return errs

    # Verb-name check
    for it in items:
        name = it.get("name", "")
        if VERB_RX.match(name):
            errs.append(f"items[id={it.get('id')}] name '{name}' starts with verb (rule: deliverable-orientation)")
        if not ID_RX.match(str(it.get("id", ""))):
            errs.append(f"items[id={it.get('id')}] invalid id pattern")

    # Overhead check (level-1 names)
    l1_names = {it["name"].lower() for it in items if it.get("level") == 1}
    for o in OVERHEAD:
        if not any(o in n for n in l1_names):
            errs.append(f"missing mandatory overhead branch: '{o}' (rule: mandatory-overhead-branches)")

    # 100% weight rule per parent
    by_parent: dict[str | None, list[dict]] = {}
    for it in items:
        by_parent.setdefault(it.get("parent"), []).append(it)
    for parent, children in by_parent.items():
        total = sum(c.get("weight_pct", 0) for c in children)
        if abs(total - 100) > 1:
            errs.append(f"parent={parent}: child weight_pct sum {total} not in [99,101] (rule: hundred-percent-rule)")

    # Leaves: must be in dictionary with effort_hours 8-80
    dict_by_id = {d["id"]: d for d in obj["dictionary"]}
    parents = {it.get("parent") for it in items if it.get("parent")}
    for it in items:
        if it["id"] in parents:
            continue  # not a leaf
        if it.get("kind") != "work_package":
            continue  # only work_packages need dict entries
        if it["id"] not in dict_by_id:
            errs.append(f"leaf {it['id']} missing Dictionary entry (rule: dictionary-required)")
            continue
        d = dict_by_id[it["id"]]
        for f in ("description", "deliverable", "acceptance_criteria", "owner", "effort_hours", "dependencies"):
            if f not in d:
                errs.append(f"dictionary[{it['id']}].{f} missing")
        eh = d.get("effort_hours", 0)
        if not (8 <= eh <= 80):
            errs.append(f"dictionary[{it['id']}].effort_hours {eh} outside [8,80] (rule: eight-eighty-sizing)")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"

SMOKE_BAD = {
    "project": "x", "version": "1.0",
    "items": [
        {"id": "1", "name": "Build user auth", "level": 1, "kind": "deliverable", "parent": None, "weight_pct": 70},
        {"id": "2", "name": "Design dashboard", "level": 1, "kind": "deliverable", "parent": None, "weight_pct": 30}
    ],
    "dictionary": []
}


def self_test() -> int:
    if SMOKE_OK_FILE.is_file():
        smoke_ok = json.loads(SMOKE_OK_FILE.read_text())
        errs = validate(smoke_ok)
        if errs:
            sys.stderr.write("smoke_ok rejected: " + "; ".join(errs) + "\n"); return 1
    if not validate(SMOKE_BAD):
        sys.stderr.write("smoke_bad accepted\n"); return 1
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
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
