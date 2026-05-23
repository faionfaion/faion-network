#!/usr/bin/env python3
"""validate-go-concurrency-patterns.py

Validate the artefact for the go-concurrency-patterns methodology against the JSON Schema
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

REQUIRED = ["package_path", "pool_size", "context_used", "errgroup_used", "unbounded_spawns", "closed_by_receiver"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'pool_size' in obj and (not isinstance(obj['pool_size'], int) or obj['pool_size'] < 1):
        errs.append('pool_size must be int >= 1')
    if 'package_path' in obj and (not isinstance(obj['package_path'], str) or len(obj['package_path']) < 3):
        errs.append('package_path must be >= 3 chars')
    if 'unbounded_spawns' in obj and obj['unbounded_spawns'] != 0:
        errs.append('unbounded_spawns must be 0')
    if 'closed_by_receiver' in obj and obj['closed_by_receiver'] != 0:
        errs.append('closed_by_receiver must be 0')
    return errs


OK = {'package_path': 'internal/worker', 'pool_size': 8, 'context_used': True, 'errgroup_used': True, 'unbounded_spawns': 0, 'closed_by_receiver': 0, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'package_path': 'x', 'pool_size': 0, 'unbounded_spawns': 3, 'closed_by_receiver': 1}


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
