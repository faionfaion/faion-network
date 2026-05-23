#!/usr/bin/env python3
"""validate-feature-flags.py

Validate the artefact for the feature-flags methodology against the JSON Schema
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

REQUIRED = ["flag_key", "owner", "created_at", "expires_at", "default_variant", "variants", "cleanup_pr_url"]


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append("missing required field: " + k)
    import re
    if 'flag_key' in obj and not re.match(r'^[a-z][a-z0-9_]+$', str(obj['flag_key'])):
        errs.append('flag_key must be snake_case')
    if 'owner' in obj and '@' not in str(obj.get('owner', '')):
        errs.append('owner must be email')
    if 'variants' in obj and (not isinstance(obj['variants'], list) or len(obj['variants']) < 2):
        errs.append('variants must be list with >= 2 items')
    if 'cleanup_pr_url' in obj and not str(obj.get('cleanup_pr_url', '')).startswith(('http://', 'https://')):
        errs.append('cleanup_pr_url must start with http:// or https://')
    return errs


OK = {'flag_key': 'new_checkout_flow', 'owner': 'team-payments@example.com', 'created_at': '2026-05-23', 'expires_at': '2026-08-23', 'default_variant': 'off', 'variants': ['off', 'on'], 'is_kill_switch': False, 'cleanup_pr_url': 'https://github.com/example/repo/pull/123'}
BAD = {'flag_key': 'NewCheckoutFlow', 'owner': 'someone', 'variants': ['on']}


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
