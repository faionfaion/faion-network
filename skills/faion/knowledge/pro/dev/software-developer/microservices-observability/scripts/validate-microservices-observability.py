#!/usr/bin/env python3
"""validate-microservices-observability.py

Validate the spec artefact for the microservices-observability methodology against the schema in
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

REQUIRED = ['service_name', 'logs_structured', 'metrics_red', 'tracing_otel', 'propagator', 'log_trace_id_present']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'service_name': 'order-service', 'logs_structured': True, 'metrics_red': True, 'tracing_otel': True, 'propagator': 'w3c', 'log_trace_id_present': True, 'otlp_endpoint': 'https://otlp.example.com:4317', 'slo_targets': {'availability': 99.9, 'p99_latency_ms': 250}, 'pii_in_spans': False}
BAD = {'logs_structured': False, 'metrics_red': False, 'tracing_otel': True, 'propagator': 'b3-fallback', 'log_trace_id_present': False, 'otlp_endpoint': 'stdout', 'pii_in_spans': True}


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
