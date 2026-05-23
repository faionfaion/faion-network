#!/usr/bin/env python3
"""validate-go-project-structure.py

Validate the artefact for the go-project-structure methodology against the JSON Schema
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

REQUIRED = ["module_path", "cmd_binaries", "internal_packages", "pkg_packages", "top_level_loose_files", "cycles_detected"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    import re
    if 'module_path' in obj and not re.match(r'^[a-z0-9./_-]+$', str(obj['module_path'])):
        errs.append('module_path must be lowercase identifier')
    if 'cmd_binaries' in obj and (not isinstance(obj['cmd_binaries'], int) or obj['cmd_binaries'] < 1):
        errs.append('cmd_binaries must be int >= 1')
    if 'internal_packages' in obj and (not isinstance(obj['internal_packages'], int) or obj['internal_packages'] < 1):
        errs.append('internal_packages must be int >= 1')
    if 'top_level_loose_files' in obj and obj['top_level_loose_files'] != 0:
        errs.append('top_level_loose_files must be 0')
    if 'cycles_detected' in obj and obj['cycles_detected'] != 0:
        errs.append('cycles_detected must be 0')
    return errs


OK = {'module_path': 'github.com/acme/payments', 'cmd_binaries': 2, 'internal_packages': 11, 'pkg_packages': 0, 'top_level_loose_files': 0, 'cycles_detected': 0, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'module_path': 'X', 'cmd_binaries': 0, 'internal_packages': 0, 'top_level_loose_files': 4, 'cycles_detected': 2}


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
