#!/usr/bin/env python3
"""validate-lessons-learned.py

Validate a report artefact for Lessons Learned against the schema in
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

REQUIRED = ['project_id', 'milestone', 'report_date', 'blameless', 'observations', 'themes', 'action_items', 'published_at']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("blameless") is not True:
        errs.append("blameless must be true")
    obs = obj.get("observations") or []
    if not obs:
        errs.append("observations must be non-empty (post-hoc retro forbidden)")
    ai = obj.get("action_items") or []
    if not ai:
        errs.append("action_items must be non-empty")
    else:
        for i, a in enumerate(ai):
            for k in ("lesson", "owner", "due_date", "acceptance_criterion"):
                if k not in a:
                    errs.append(f"action_items[{i}].{k} missing")
    if not obj.get("themes"):
        errs.append("themes empty")

    return errs


GOOD = {'project_id': 'acme', 'milestone': 'M3', 'report_date': '2026-05-20', 'blameless': True, 'observations': [{'date': '2026-05-10', 'observer': 'U', 'signal': 'x', 'hypothesis': 'y'}], 'themes': ['cert lifecycle'], 'action_items': [{'lesson': 'monitor cert', 'owner': 'U_OPS', 'due_date': '2026-06-15', 'acceptance_criterion': 'alert fires'}], 'published_at': '2026-05-22T10:00:00Z'}
BAD = {'project_id': 'x', 'milestone': 'y', 'report_date': 'z', 'blameless': False, 'observations': [], 'themes': [], 'action_items': [{'lesson': 'do better'}], 'published_at': ''}


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
