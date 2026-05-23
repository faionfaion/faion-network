#!/usr/bin/env python3
"""validate-lb-health-checks.py

Validate the health-check artefact against the schema in 02-output-contract.xml.

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
    "liveness_path",
    "readiness_path",
    "readiness_deps",
    "interval_sec",
    "healthy_threshold",
    "unhealthy_threshold",
    "lb_expect_status",
]


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("liveness_path") and obj.get("liveness_path") == obj.get("readiness_path"):
        errs.append("liveness_path must differ from readiness_path")
    deps = obj.get("readiness_deps", [])
    if not isinstance(deps, list) or len(deps) == 0:
        errs.append("readiness_deps must be non-empty list")
    else:
        for i, d in enumerate(deps):
            if not isinstance(d, dict) or "timeout_sec" not in d:
                errs.append(f"readiness_deps[{i}].timeout_sec required")
            else:
                t = d.get("timeout_sec", 0)
                if not (1 <= t <= 10):
                    errs.append(f"readiness_deps[{i}].timeout_sec must be 1-10")
    if obj.get("interval_sec", 0) < 10:
        errs.append("interval_sec must be >= 10")
    if obj.get("healthy_threshold", 0) < 2:
        errs.append("healthy_threshold must be >= 2")
    if obj.get("unhealthy_threshold", 0) < 2:
        errs.append("unhealthy_threshold must be >= 2")
    if obj.get("lb_expect_status") != 200:
        errs.append("lb_expect_status must equal 200")
    return errs


OK = {
    "liveness_path": "/health/live",
    "readiness_path": "/health/ready",
    "readiness_deps": [
        {"name": "postgres", "timeout_sec": 3},
        {"name": "redis", "timeout_sec": 2},
    ],
    "interval_sec": 10,
    "healthy_threshold": 2,
    "unhealthy_threshold": 3,
    "lb_expect_status": 200,
    "lb_kind": "kubernetes",
}
BAD = {
    "liveness_path": "/health",
    "readiness_path": "/health",
    "readiness_deps": [],
    "interval_sec": 1,
    "healthy_threshold": 1,
    "unhealthy_threshold": 1,
    "lb_expect_status": 0,
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
