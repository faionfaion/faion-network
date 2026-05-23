#!/usr/bin/env python3
"""validate-lb-monitoring.py

Validate the LB monitoring artefact against the schema in 02-output-contract.xml.

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

REQUIRED = [
    "lb_kind",
    "exporter",
    "alerts",
    "per_backend_label",
    "log_destination",
    "dashboard_templated",
]
EXPECTED_ALERTS = {
    "BackendDown",
    "HighErrorRate",
    "HighLatency",
    "ConnectionPoolExhausted",
}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not obj.get("exporter"):
        errs.append("exporter must be set")
    alerts = obj.get("alerts", []) or []
    names = {a.get("name") for a in alerts if isinstance(a, dict)}
    missing = EXPECTED_ALERTS - names
    if missing:
        errs.append(f"missing alerts: {sorted(missing)}")
    for a in alerts:
        if not isinstance(a, dict):
            continue
        if a.get("for_seconds", 0) < 60:
            errs.append(f"alert {a.get('name')!r} has for_seconds < 60")
    if obj.get("per_backend_label") is not True:
        errs.append("per_backend_label must be true")
    if not obj.get("log_destination"):
        errs.append("log_destination must be set")
    if obj.get("log_retention_days", 0) < 30:
        errs.append("log_retention_days must be >= 30")
    if obj.get("dashboard_templated") is not True:
        errs.append("dashboard_templated must be true")
    return errs


OK = {
    "lb_kind": "haproxy",
    "exporter": "haproxy-exporter",
    "alerts": [
        {"name": "BackendDown", "for_seconds": 60},
        {"name": "HighErrorRate", "for_seconds": 300},
        {"name": "HighLatency", "for_seconds": 300},
        {"name": "ConnectionPoolExhausted", "for_seconds": 120},
    ],
    "per_backend_label": True,
    "log_destination": "loki",
    "log_retention_days": 30,
    "dashboard_templated": True,
}
BAD = {
    "lb_kind": "haproxy",
    "exporter": "",
    "alerts": [],
    "per_backend_label": False,
    "log_destination": "",
    "log_retention_days": 1,
    "dashboard_templated": False,
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
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
