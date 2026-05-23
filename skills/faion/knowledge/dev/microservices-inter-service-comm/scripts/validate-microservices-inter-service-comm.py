#!/usr/bin/env python3
"""validate-microservices-inter-service-comm.py

Validate the decision-record artefact for the microservices-inter-service-comm methodology against the schema in
02-output-contract.xml.

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

REQUIRED = ['call_name', 'caller', 'downstream', 'style', 'schema_registered_at', 'idempotency_key_supported']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'call_name': 'order-created-event', 'caller': 'order-service', 'downstream': 'billing,shipping,analytics', 'style': 'async-kafka', 'latency_budget_ms': 60000, 'p99_downstream_ms': 100, 'schema_registered_at': 'https://schema-registry.example.com/order-created/v1', 'idempotency_key_supported': True, 'fan_out_consumers': 3}
BAD = {'caller': 'order-service', 'downstream': 'billing', 'style': 'rest', 'latency_budget_ms': 100, 'p99_downstream_ms': 300, 'schema_registered_at': 'inline-in-controller', 'idempotency_key_supported': False, 'fan_out_consumers': 3}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
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
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
