#!/usr/bin/env python3
"""validate-lb-haproxy-production.py

Validate the HAProxy config artefact against the schema in 02-output-contract.xml.

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
    "tls_version_min",
    "stick_table_rate_limit",
    "nbthread",
    "maxconn",
    "http_check_expect",
    "ha_mode",
]


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("tls_version_min") not in ("TLSv1.2", "TLSv1.3"):
        errs.append("tls_version_min must be TLSv1.2 or TLSv1.3")
    rl = obj.get("stick_table_rate_limit", {})
    if not isinstance(rl, dict) or not rl.get("enabled"):
        errs.append("stick_table_rate_limit.enabled must be true")
    if not (isinstance(obj.get("nbthread"), int) and obj["nbthread"] >= 1):
        errs.append("nbthread must be >= 1")
    if not (isinstance(obj.get("maxconn"), int) and obj["maxconn"] >= 100):
        errs.append("maxconn must be >= 100")
    if obj.get("http_check_expect") is not True:
        errs.append("http_check_expect must be true")
    return errs


OK = {
    "tls_version_min": "TLSv1.2",
    "stick_table_rate_limit": {"enabled": True, "threshold_per_10s": 100},
    "nbthread": 8,
    "cpu_map_auto": True,
    "maxconn": 200000,
    "http_check_expect": True,
    "ha_mode": "keepalived-vrrp",
}
BAD = {
    "tls_version_min": "TLSv1.0",
    "stick_table_rate_limit": {"enabled": False, "threshold_per_10s": 0},
    "nbthread": 1,
    "maxconn": 0,
    "http_check_expect": False,
    "ha_mode": "single",
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
