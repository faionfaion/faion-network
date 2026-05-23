#!/usr/bin/env python3
"""validate-lb-algorithms.py

Validate the config artefact for the lb-algorithms methodology against the schema
in 02-output-contract.xml.

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

ALGORITHMS = {
    "round-robin",
    "weighted-round-robin",
    "least-connections",
    "weighted-least-connections",
    "least-response-time",
    "ip-hash",
    "cookie-sticky",
    "resource-based",
}
REQUIRED = [
    "algorithm",
    "fleet_capacity",
    "request_cost",
    "autoscaling",
    "nat_behind_lb",
    "measured",
]


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    algo = obj.get("algorithm")
    if algo not in ALGORITHMS:
        errs.append(f"algorithm must be one of {sorted(ALGORITHMS)}")
    if algo == "ip-hash" and (obj.get("autoscaling") or obj.get("nat_behind_lb")):
        errs.append("ip-hash forbidden with autoscaling or NAT")
    if algo == "round-robin" and obj.get("fleet_capacity") == "heterogeneous":
        errs.append("round-robin forbidden on heterogeneous fleet")
    if algo == "round-robin" and obj.get("request_cost") == "variable":
        errs.append("round-robin forbidden on variable-cost workload")
    m = obj.get("measured", {})
    if not isinstance(m, dict) or "p50_ms" not in m or "p99_ms" not in m:
        errs.append("measured.{p50_ms,p99_ms} required")
    if obj.get("fleet_capacity") == "heterogeneous":
        w = obj.get("weights")
        if not isinstance(w, list) or len(w) == 0:
            errs.append("weights required on heterogeneous fleet")
    return errs


OK = {
    "algorithm": "weighted-least-connections",
    "fleet_capacity": "heterogeneous",
    "request_cost": "variable",
    "autoscaling": True,
    "nat_behind_lb": False,
    "measured": {"p50_ms": 80, "p99_ms": 240},
    "weights": [100, 100, 50],
    "rationale": "p99/p50 = 3x; heterogeneous fleet; leastconn + weights.",
}
BAD = {
    "algorithm": "ip-hash",
    "fleet_capacity": "homogeneous",
    "request_cost": "uniform",
    "autoscaling": True,
    "nat_behind_lb": True,
    "measured": {"p50_ms": 50, "p99_ms": 55},
    "rationale": "wanted sticky",
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
