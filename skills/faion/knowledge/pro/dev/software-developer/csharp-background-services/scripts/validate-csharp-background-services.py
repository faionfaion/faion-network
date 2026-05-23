#!/usr/bin/env python3
"""validate-csharp-background-services.py

Validate a worker-spec artefact against the schema in 02-output-contract.xml.

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
import re
import sys
from pathlib import Path

REQUIRED = [
    "worker_class",
    "channel",
    "scope_strategy",
    "stopping_token_propagated",
    "exception_handling",
    "health_check",
]
CLASS_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Service$")
FULL_MODES = {"Wait", "DropOldest", "DropNewest"}
SCOPE_STRATS = {"create-scope-per-item", "no-scoped-deps"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "worker_class" in obj and not CLASS_RE.match(str(obj["worker_class"])):
        errs.append("worker_class must be PascalCase ending in 'Service'")
    if obj.get("base_class") and obj["base_class"] != "BackgroundService":
        errs.append("base_class must be 'BackgroundService' (not IHostedService)")
    ch = obj.get("channel") or {}
    if ch.get("mode") == "bounded":
        if not isinstance(ch.get("capacity"), int) or ch["capacity"] < 1:
            errs.append("channel.capacity must be int >= 1 when mode=bounded")
        if ch.get("full_mode") not in FULL_MODES:
            errs.append(f"channel.full_mode must be one of {sorted(FULL_MODES)}")
    if obj.get("scope_strategy") not in SCOPE_STRATS:
        errs.append(f"scope_strategy must be one of {sorted(SCOPE_STRATS)}")
    if obj.get("stopping_token_propagated") is not True:
        errs.append("stopping_token_propagated must be true")
    if obj.get("exception_handling") != "try-catch-per-item":
        errs.append("exception_handling must be 'try-catch-per-item'")
    hc = obj.get("health_check") or {}
    if "registered" not in hc:
        errs.append("health_check.registered required")
    return errs


OK = {
    "worker_class": "OrderProcessorService",
    "base_class": "BackgroundService",
    "channel": {"mode": "bounded", "capacity": 1000, "full_mode": "Wait"},
    "scope_strategy": "create-scope-per-item",
    "stopping_token_propagated": True,
    "exception_handling": "try-catch-per-item",
    "health_check": {"registered": True, "stale_after_seconds": 300},
}
BAD = {
    "worker_class": "orderWorker",
    "base_class": "IHostedService",
    "channel": {"mode": "bounded", "capacity": 0, "full_mode": "Nope"},
    "scope_strategy": "no-scoped-deps",
    "stopping_token_propagated": False,
    "exception_handling": "try-catch-per-item",
    "health_check": {},
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
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
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
