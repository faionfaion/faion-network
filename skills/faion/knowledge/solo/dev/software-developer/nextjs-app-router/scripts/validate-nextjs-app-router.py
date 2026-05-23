#!/usr/bin/env python3
"""validate-nextjs-app-router.py

Validate the artefact for the nextjs-app-router methodology against the JSON Schema
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

REQUIRED = ["app_dir", "server_components_count", "client_components_count", "server_actions_count", "fetch_in_client_components", "api_routes_for_mutations"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    if 'app_dir' in obj and (not isinstance(obj['app_dir'], str) or len(obj['app_dir']) < 1):
        errs.append('app_dir must be non-empty')
    if 'server_components_count' in obj and (not isinstance(obj['server_components_count'], int) or obj['server_components_count'] < 1):
        errs.append('server_components_count must be int >= 1')
    if 'fetch_in_client_components' in obj and obj['fetch_in_client_components'] != 0:
        errs.append('fetch_in_client_components must be 0')
    if 'api_routes_for_mutations' in obj and obj['api_routes_for_mutations'] != 0:
        errs.append('api_routes_for_mutations must be 0')
    return errs


OK = {'app_dir': 'app/', 'server_components_count': 42, 'client_components_count': 11, 'server_actions_count': 8, 'fetch_in_client_components': 0, 'api_routes_for_mutations': 0, 'validated_at': '2026-05-23T10:00:00Z'}
BAD = {'app_dir': '', 'server_components_count': 0, 'fetch_in_client_components': 14, 'api_routes_for_mutations': 5}


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
