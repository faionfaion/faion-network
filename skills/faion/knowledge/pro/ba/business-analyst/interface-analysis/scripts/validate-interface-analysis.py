#!/usr/bin/env python3
"""validate-interface-analysis.py

Validate a spec artefact produced by the interface-analysis methodology
against the JSON Schema captured in content/02-output-contract.xml.

stdlib-only. Inputs / outputs / exit codes documented under --help.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixture
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

REQUIRED = ['interface_id', 'name', 'type', 'data_elements', 'protocol', 'frequency', 'volume', 'security', 'error_handling', 'owner']


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"interface_id": "IF-0012", "name": "Order events to billing", "type": "system", "data_elements": [{"name": "order_id", "type": "string", "direction": "out"}], "protocol": {"name": "kafka", "version": "3.6"}, "frequency": "continuous", "volume": {"records_per_day": 250000, "peak_per_minute": 600}, "security": {"authn": "mTLS", "authz": "RBAC", "encryption_in_transit": "TLS1.3", "encryption_at_rest": "AES-256", "data_classification": "PII"}, "error_handling": {"retry": "exp-backoff", "dlq": "kafka:billing.dlq", "alerting": "pagerduty:billing-on-call"}, "owner": "Order Platform"}')
BAD = json.loads('{"interface_id": "IF1", "name": "events"}')


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: good fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: bad fixture accepted\n")
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
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"VIOLATION: invalid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
