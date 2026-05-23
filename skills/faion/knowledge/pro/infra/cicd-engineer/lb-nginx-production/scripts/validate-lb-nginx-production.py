#!/usr/bin/env python3
"""validate-lb-nginx-production.py

Validate the Nginx LB config artefact against the schema in 02-output-contract.xml.

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
    "worker_processes",
    "worker_rlimit_nofile",
    "upstream_zone",
    "upstream_keepalive",
    "tls_min",
    "limit_req_zone",
    "security_headers",
]


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("worker_processes") != "auto":
        errs.append("worker_processes must equal auto")
    if obj.get("worker_rlimit_nofile", 0) < 65535:
        errs.append("worker_rlimit_nofile must be >= 65535")
    if obj.get("upstream_zone") is not True:
        errs.append("upstream_zone must be true")
    if obj.get("upstream_keepalive", 0) < 16:
        errs.append("upstream_keepalive must be >= 16")
    if obj.get("tls_min") not in ("TLSv1.2", "TLSv1.3"):
        errs.append("tls_min must be TLSv1.2 or TLSv1.3")
    rl = obj.get("limit_req_zone", {})
    if not isinstance(rl, dict) or rl.get("rate_per_sec", 0) < 1:
        errs.append("limit_req_zone.rate_per_sec must be >= 1")
    hdrs = obj.get("security_headers", [])
    if not isinstance(hdrs, list) or len(hdrs) < 5:
        errs.append("security_headers must list >= 5 entries")
    return errs


OK = {
    "worker_processes": "auto",
    "worker_rlimit_nofile": 65535,
    "upstream_zone": True,
    "upstream_keepalive": 32,
    "tls_min": "TLSv1.2",
    "ssl_stapling": True,
    "limit_req_zone": {"rate_per_sec": 10},
    "security_headers": [
        "HSTS",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
        "Permissions-Policy",
    ],
}
BAD = {
    "worker_processes": "1",
    "worker_rlimit_nofile": 1024,
    "upstream_zone": False,
    "upstream_keepalive": 0,
    "tls_min": "TLSv1.0",
    "ssl_stapling": False,
    "limit_req_zone": {"rate_per_sec": 0},
    "security_headers": [],
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
