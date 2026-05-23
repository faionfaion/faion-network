#!/usr/bin/env python3
"""validate-fast-vs-slow-burn-rule.py

Validate an artefact produced by the Fast vs Slow Burn Rule methodology
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

REQUIRED = ['alertmanager_routes', 'runbook_urls', 'sli_recording_rule_prefix', 'slo_id', 'slo_target', 'windows']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'slo_id': 'checkout-api-availability-30d', 'slo_target': 0.999, 'windows': [{'length': '1h', 'burn_rate_threshold': 14.4, 'routing': 'page'}, {'length': '6h', 'burn_rate_threshold': 6.0, 'routing': 'page'}, {'length': '3d', 'burn_rate_threshold': 1.0, 'routing': 'ticket'}, {'length': '30d', 'burn_rate_threshold': 0.1, 'routing': 'review'}], 'sli_recording_rule_prefix': 'level:checkout_api:slo', 'alertmanager_routes': {'1h': 'oncall-page', '6h': 'oncall-page', '3d': 'slo-tickets', '30d': 'slo-review'}, 'runbook_urls': {'1h': 'https://runbooks/api-availability-1h', '6h': 'https://runbooks/api-availability-6h', '3d': 'https://runbooks/api-availability-3d', '30d': 'https://runbooks/api-availability-30d'}}
BAD = {'slo_id': 'checkout-api', 'slo_target': 0.999, 'windows': [{'length': '1h', 'burn_rate_threshold': 5.0, 'routing': 'page'}], 'runbook_urls': {}}


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
