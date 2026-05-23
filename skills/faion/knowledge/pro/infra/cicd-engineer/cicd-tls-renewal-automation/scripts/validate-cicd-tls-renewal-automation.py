#!/usr/bin/env python3
"""validate-cicd-tls-renewal-automation.py

Validate the artefact for the cicd-tls-renewal-automation methodology against the JSON Schema in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['acme_client', 'scheduler', 'challenge', 'deploy_hook', 'expiry_alert_days', 'staging_validated']

ENUMS = { 'acme_client': ['certbot', 'acme.sh', 'lego', 'traefik-acme'], 'challenge': ['http-01', 'dns-01', 'tls-alpn-01'] }
CONSTS = { 'scheduler': 'systemd-timer' }
INT_BOUNDS = { 'expiry_alert_days': (7, 30) }
ARRAY_MIN = {  }
OBJECT_REQUIRED = {  }


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k, allowed in ENUMS.items():
        if k in obj and obj[k] not in allowed:
            errs.append(f"{k} must be one of {allowed}")
    for k, expected in CONSTS.items():
        if k in obj and obj[k] != expected:
            errs.append(f"{k} must equal {expected!r}")
    for k, (lo, hi) in INT_BOUNDS.items():
        if k in obj:
            v = obj[k]
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                errs.append(f"{k} must be a number")
                continue
            if lo is not None and v < lo:
                errs.append(f"{k} must be >= {lo}")
            if hi is not None and v > hi:
                errs.append(f"{k} must be <= {hi}")
    for k, minitems in ARRAY_MIN.items():
        if k in obj:
            if not isinstance(obj[k], list):
                errs.append(f"{k} must be array")
            elif len(obj[k]) < minitems:
                errs.append(f"{k} must have >= {minitems} items")
    for k, req in OBJECT_REQUIRED.items():
        if k in obj:
            v = obj[k]
            if not isinstance(v, dict):
                errs.append(f"{k} must be object")
                continue
            for rk in req:
                if rk not in v:
                    errs.append(f"{k}.{rk} missing")
    return errs


OK = {'acme_client': 'certbot', 'scheduler': 'systemd-timer', 'challenge': 'http-01', 'deploy_hook': 'ok', 'expiry_alert_days': 7, 'staging_validated': True}
BAD = {'acme_client': None}


def self_test():
    if validate(OK):
        sys.stderr.write("ok rejected: " + str(validate(OK)) + "\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    if isinstance(obj, dict):
        obj.pop("__faion_header__", None)
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
