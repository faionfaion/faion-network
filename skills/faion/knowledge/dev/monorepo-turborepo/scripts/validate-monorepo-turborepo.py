#!/usr/bin/env python3
"""validate-monorepo-turborepo.py

Validate the artefact for the monorepo-turborepo methodology against the JSON Schema
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
import sys
from pathlib import Path

REQUIRED = ["workspace_root", "package_count", "task_count", "floating_versions", "tasks_without_outputs", "remote_cache_in_ci"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'package_count' in obj and (not isinstance(obj['package_count'], int) or obj['package_count'] < 2):
        errs.append('package_count must be int >= 2')
    if 'task_count' in obj and (not isinstance(obj['task_count'], int) or obj['task_count'] < 1):
        errs.append('task_count must be int >= 1')
    if 'floating_versions' in obj and obj['floating_versions'] != 0:
        errs.append('floating_versions must be 0')
    if 'tasks_without_outputs' in obj and obj['tasks_without_outputs'] != 0:
        errs.append('tasks_without_outputs must be 0')
    if 'workspace_root' in obj and (not isinstance(obj['workspace_root'], str) or len(obj['workspace_root']) < 1):
        errs.append('workspace_root must be non-empty')
    return errs


OK = {'workspace_root': '/', 'package_count': 7, 'task_count': 5, 'floating_versions': 0, 'tasks_without_outputs': 0, 'remote_cache_in_ci': True, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'workspace_root': '', 'package_count': 1, 'floating_versions': 42, 'tasks_without_outputs': 3}


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
