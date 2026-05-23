#!/usr/bin/env python3
"""validate-lb-high-availability.py

Validate the HA decision-record artefact against the schema in 02-output-contract.xml.

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
    "sla_target",
    "lb_instances",
    "azs_used",
    "backends_per_az",
    "gslb_kind",
    "drain_on_sigterm",
]


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("lb_instances", 0) < 2:
        errs.append("lb_instances must be >= 2")
    if obj.get("azs_used", 0) < 2:
        errs.append("azs_used must be >= 2")
    if obj.get("backends_per_az", 0) < 2:
        errs.append("backends_per_az must be >= 2")
    if obj.get("sla_target") in ("99.99", "99.999") and obj.get("gslb_kind") == "dns-based":
        errs.append("dns-based GSLB forbidden at sla_target >= 99.99")
    if obj.get("drain_on_sigterm") is not True:
        errs.append("drain_on_sigterm must be true")
    if obj.get("deregistration_delay_sec", 0) < 30:
        errs.append("deregistration_delay_sec must be >= 30")
    return errs


OK = {
    "sla_target": "99.99",
    "lb_instances": 2,
    "azs_used": 3,
    "backends_per_az": 2,
    "gslb_kind": "anycast",
    "drain_on_sigterm": True,
    "deregistration_delay_sec": 30,
    "failure_modes_documented": True,
    "adr_path": ".aidocs/decisions/ha-payments.md",
}
BAD = {
    "sla_target": "99.99",
    "lb_instances": 1,
    "azs_used": 1,
    "backends_per_az": 1,
    "gslb_kind": "dns-based",
    "drain_on_sigterm": False,
    "deregistration_delay_sec": 0,
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
