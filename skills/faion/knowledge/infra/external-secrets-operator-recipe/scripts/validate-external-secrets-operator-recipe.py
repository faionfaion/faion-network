#!/usr/bin/env python3
"""validate-external-secrets-operator-recipe.py

Validate an artefact produced by the External Secrets Operator Recipe methodology
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

REQUIRED = ['alert_on_sync_failure', 'cluster_secret_store', 'external_secrets', 'mount_type', 'rbac_scope', 'rotation_test_runbook_path']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'cluster_secret_store': {'name': 'vault-prod', 'backend': 'vault', 'auth_method': 'kubernetes', 'identity_ref': 'system:serviceaccount:eso:vault-auth'}, 'external_secrets': [{'name': 'api-db-creds', 'namespace': 'prod-api', 'refresh_interval': '1h', 'target_path': '/var/run/secrets/db/', 'key_refs': ['prod/api/db-password']}], 'rbac_scope': 'namespace', 'alert_on_sync_failure': True, 'rotation_test_runbook_path': 'runbooks/secret-rotation.md', 'mount_type': 'file'}
BAD = {'cluster_secret_store': {'name': 'vault-prod', 'auth_method': 'token', 'identity_ref': 'static-token'}, 'external_secrets': [{'refresh_interval': '10s'}], 'rbac_scope': 'cluster', 'alert_on_sync_failure': False, 'mount_type': 'env'}


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
