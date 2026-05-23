#!/usr/bin/env python3
"""validate-api-monitoring-alerting.py

Validate the artefact for api-monitoring-alerting against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (rc=0 if both pass)
    --help            this message

Exit codes:
    0 = valid (or self-test passed)
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['slo', 'burn_rate_rules', 'routing', 'dashboards_as_code']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK_FIXTURE = '{"slo": {"target_percent": 99.9, "window_days": 30, "error_budget_percent": 0.1}, "burn_rate_rules": [{"name": "page-fast-burn", "for": "5m", "severity": "page", "runbook_url": "https://runbooks.faion.net/api-slo", "burn_rate_short": "1h-2%", "burn_rate_long": "6h-5%"}, {"name": "ticket-slow-burn", "for": "30m", "severity": "ticket", "runbook_url": "https://runbooks.faion.net/api-slo", "burn_rate_short": "1d-10%", "burn_rate_long": "3d-10%"}], "routing": {"page_to": "pagerduty:api-oncall", "ticket_to": "jira:API"}, "dashboards_as_code": true}'
BAD_FIXTURE = '{"burn_rate_rules": [{"name": "errors-1pct", "for": "0s", "severity": "page"}], "routing": {"page_to": "", "ticket_to": ""}, "dashboards_as_code": false}'


def self_test() -> int:
    """Built-in fixtures: OK_FIXTURE accepted, BAD_FIXTURE rejected."""
    if validate(json.loads(OK_FIXTURE)):
        sys.stderr.write("self-test FAIL: valid fixture rejected\n")
        return 1
    if not validate(json.loads(BAD_FIXTURE)):
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
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
