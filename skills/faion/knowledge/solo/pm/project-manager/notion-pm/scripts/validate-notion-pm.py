#!/usr/bin/env python3
"""validate-notion-pm.py

Validate the artefact for the notion-pm methodology against the JSON Schema
in content/02-output-contract.xml.

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

UUID_RE = re.compile(r"^[0-9a-f-]{36}$")
REQUIRED = [
    "projects_db_id",
    "tasks_db_id",
    "sprints_db_id",
    "properties_per_db",
    "uses_rollups",
    "archive_cutoff_days",
    "rate_limit_per_sec",
]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    for k in ("projects_db_id", "tasks_db_id", "sprints_db_id"):
        v = obj.get(k)
        if v is not None and (not isinstance(v, str) or not UUID_RE.match(v)):
            errs.append(k + " must be UUID string")
    props = obj.get("properties_per_db")
    if isinstance(props, dict):
        for sub in ("projects", "tasks", "sprints"):
            if sub not in props:
                errs.append("properties_per_db missing: " + sub)
            else:
                n = props[sub]
                if not isinstance(n, int) or n < 1 or n > 20:
                    errs.append("properties_per_db." + sub + " must be int 1..20")
    elif "properties_per_db" in obj:
        errs.append("properties_per_db must be object")
    if obj.get("uses_rollups") is not True:
        errs.append("uses_rollups must be true")
    rl = obj.get("rate_limit_per_sec")
    if rl is not None and (not isinstance(rl, (int, float)) or rl <= 0 or rl > 3):
        errs.append("rate_limit_per_sec must be 0<x<=3")
    cutoff = obj.get("archive_cutoff_days")
    if cutoff is not None and (not isinstance(cutoff, int) or cutoff < 30 or cutoff > 365):
        errs.append("archive_cutoff_days must be int 30..365")
    atc = obj.get("active_task_count")
    if atc is not None and (not isinstance(atc, int) or atc < 0 or atc > 500):
        errs.append("active_task_count must be 0..500")
    return errs


OK = {
    "projects_db_id": "11111111-1111-1111-1111-111111111111",
    "tasks_db_id": "22222222-2222-2222-2222-222222222222",
    "sprints_db_id": "33333333-3333-3333-3333-333333333333",
    "properties_per_db": {"projects": 12, "tasks": 18, "sprints": 9},
    "uses_rollups": True,
    "uses_status_property": True,
    "archive_cutoff_days": 90,
    "active_task_count": 312,
    "rate_limit_per_sec": 2.5,
    "validated_at": "2026-05-23T10:00:00Z",
}
BAD = {
    "projects_db_id": "not-a-uuid",
    "tasks_db_id": "22222222-2222-2222-2222-222222222222",
    "properties_per_db": {"projects": 35, "tasks": 50, "sprints": 9},
    "uses_rollups": False,
    "archive_cutoff_days": 730,
    "rate_limit_per_sec": 50,
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
