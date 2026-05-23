#!/usr/bin/env python3
"""validate-ssl-tls-setup.py

Validate an artefact produced by the SSL/TLS Setup methodology
against the JSON Schema declared in content/02-output-contract.xml.

Inputs:
    --file PATH       path to the artefact JSON file
    --self-test       run built-in fixtures (OK + BAD) and exit 0 on pass
    --help            this message

Exit codes:
    0 = valid (or self-test pass)
    1 = invalid (or self-test fail)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['auto_renew', 'cert_source', 'cipher_suites', 'hostname', 'hsts_max_age', 'ocsp_stapling', 'post_deploy_scan_grade', 'tls_min_version']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'hostname': 'api.acme.com', 'tls_min_version': 'TLSv1.3', 'cipher_suites': ['TLS_AES_256_GCM_SHA384', 'TLS_CHACHA20_POLY1305_SHA256'], 'cert_source': 'lets_encrypt', 'auto_renew': True, 'hsts_max_age': 31536000, 'ocsp_stapling': True, 'post_deploy_scan_grade': 'A+'}
BAD = {'hostname': 'old.example.com', 'tls_min_version': 'TLSv1.0', 'cipher_suites': ['AES128-SHA'], 'cert_source': 'manual', 'auto_renew': False, 'hsts_max_age': 0, 'ocsp_stapling': False}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"self-test FAIL: OK fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
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
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
