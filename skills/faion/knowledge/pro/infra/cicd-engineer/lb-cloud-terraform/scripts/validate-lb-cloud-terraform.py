#!/usr/bin/env python3
"""validate-lb-cloud-terraform.py

Validate the Terraform LB artefact against the schema in 02-output-contract.xml.

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
    "provider",
    "lb_type",
    "deletion_protection",
    "tls_policy",
    "access_logs_bucket",
    "http_to_https_redirect",
    "security_group_tight",
]
TLS_OK = re.compile(r"^(ELBSecurityPolicy-TLS13-1-2-2021-06|MODERN|RESTRICTED)$")
TLS_OLD = re.compile(r"^ELBSecurityPolicy-2016", re.IGNORECASE)


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("deletion_protection") is not True:
        errs.append("deletion_protection must be true")
    tls = obj.get("tls_policy", "")
    if TLS_OLD.match(tls):
        errs.append("tls_policy uses outdated policy")
    if not TLS_OK.match(tls):
        errs.append("tls_policy must be modern (TLS13-1-2-2021-06|MODERN|RESTRICTED)")
    if not obj.get("access_logs_bucket"):
        errs.append("access_logs_bucket required")
    if obj.get("http_to_https_redirect") is not True:
        errs.append("http_to_https_redirect must be true")
    if obj.get("security_group_tight") is not True:
        errs.append("security_group_tight must be true")
    return errs


OK = {
    "provider": "aws",
    "lb_type": "alb",
    "deletion_protection": True,
    "tls_policy": "ELBSecurityPolicy-TLS13-1-2-2021-06",
    "access_logs_bucket": "company-alb-logs-prod",
    "http_to_https_redirect": True,
    "security_group_tight": True,
    "waf_attached": True,
    "target_health_check_path": "/health",
}
BAD = {
    "provider": "aws",
    "lb_type": "alb",
    "deletion_protection": False,
    "tls_policy": "ELBSecurityPolicy-2016-08",
    "access_logs_bucket": "",
    "http_to_https_redirect": False,
    "security_group_tight": False,
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
