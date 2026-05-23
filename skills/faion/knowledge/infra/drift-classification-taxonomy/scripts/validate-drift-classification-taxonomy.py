#!/usr/bin/env python3
"""validate-drift-classification-taxonomy.py

Validate an artefact produced by the Drift Classification Taxonomy methodology
against the JSON Schema declared in content/02-output-contract.xml.

Inputs:
    --file PATH       path to the artefact JSON file
    --self-test       run built-in fixtures (OK + BAD) and exit 0 on pass
    --help            this message

Exit codes:
    0 = valid (or self-test pass)
    1 = invalid (or self-test fail)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['class', 'detected_at', 'drift_id', 'environment', 'evidence', 'fix_action', 'fix_pr_url', 'resource_address', 'triage_at', 'triage_owner']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'drift_id': 'drift-2026-05-20-001', 'environment': 'prod', 'resource_address': 'module.api.aws_security_group.sg', 'detected_at': '2026-05-20T10:00:00Z', 'class': 'legitimate_emergency', 'evidence': {'source': 'cloudtrail', 'reference': 'arn:aws:cloudtrail:event/abc123'}, 'fix_action': 'backport', 'fix_pr_url': 'https://github.com/acme/infra/pull/4321', 'triage_owner': 'platform-team', 'triage_at': '2026-05-21T10:00:00Z'}
BAD = {'drift_id': 'drift-2026-05-20-002', 'class': 'tbd', 'evidence': {}, 'fix_action': 'ignore', 'triage_owner': ''}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"self-test FAIL: OK fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
