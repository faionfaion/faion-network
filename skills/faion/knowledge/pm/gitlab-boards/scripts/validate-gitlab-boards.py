#!/usr/bin/env python3
"""validate-gitlab-boards.py

Validate a config artefact for GitLab Issue Boards against the schema in
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

REQUIRED = ['group', 'project', 'scoped_labels', 'milestones', 'board_lists', 'token_scope']


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    sl = obj.get("scoped_labels") or {}
    if len((sl.get("status") or [])) < 3:
        errs.append("scoped_labels.status must have >=3 entries")
    ms = obj.get("milestones") or {}
    if ms.get("cadence") not in {"weekly", "biweekly", "monthly"}:
        errs.append(f"milestone cadence invalid: {ms.get('cadence')!r}")
    bl = obj.get("board_lists") or []
    for i, lst in enumerate(bl):
        v = lst.get("scoped_label_value", "")
        if not v.startswith("status::"):
            errs.append(f"board_lists[{i}].scoped_label_value not scoped: {v!r}")
    ts = obj.get("token_scope") or {}
    scope_list = ts.get("scope") or []
    if "sudo" in scope_list or "admin_mode" in scope_list:
        errs.append("token_scope contains sudo/admin_mode")
    exp = ts.get("expiry_days")
    if not isinstance(exp, int) or not (7 <= exp <= 365):
        errs.append(f"token_scope.expiry_days invalid: {exp!r}")

    return errs


GOOD = {'group': 'acme', 'project': 'p', 'scoped_labels': {'status': ['status::todo', 'status::doing', 'status::done'], 'type': ['type::bug', 'type::feature'], 'priority': ['priority::high', 'priority::low']}, 'milestones': {'cadence': 'biweekly', 'active': ['s1']}, 'board_lists': [{'name': 'Todo', 'scoped_label_value': 'status::todo'}, {'name': 'Doing', 'scoped_label_value': 'status::doing'}, {'name': 'Done', 'scoped_label_value': 'status::done'}], 'token_scope': {'scope': ['api', 'read_repository'], 'expiry_days': 90}}
BAD = {'group': 'x', 'project': 'y', 'scoped_labels': {'status': []}, 'milestones': {'cadence': 'ad-hoc', 'active': []}, 'board_lists': [{'name': 'D', 'scoped_label_value': 'doing'}], 'token_scope': {'scope': ['api', 'sudo'], 'expiry_days': 9999}}


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
