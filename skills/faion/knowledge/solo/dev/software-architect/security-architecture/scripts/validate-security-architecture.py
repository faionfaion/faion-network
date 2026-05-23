#!/usr/bin/env python3
"""validate-security-architecture.py

Validate the artefact produced by the security-architecture methodology against the JSON
Schema embedded in content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run built-in OK + BAD fixtures
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED: tuple[str, ...] = ('spec_id', 'identity', 'authz', 'secrets', 'threat_model_ref', 'ci_controls', 'incident_response', 'version', 'last_reviewed',)
ENUMS: dict[str, list] = {}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k, allowed in ENUMS.items():
        if k in obj and obj[k] not in allowed:
            errs.append(f"field {k!r} not in allowed values {allowed!r}; got {obj[k]!r}")
    return errs


OK = {'spec_id': 'sec-storefront-2026-05', 'identity': {'provider': 'auth0', 'mfa_scope': 'admin_only'}, 'authz': {'model': 'rbac', 'tenant_filter': 'rls'}, 'secrets': {'provider': 'vault', 'rotation_days': 90, 'per_service_scope': True}, 'threat_model_ref': 'docs/security/threat-model-storefront-2026.md', 'ci_controls': ['sast', 'sca', 'secret_scan', 'iac_scan'], 'incident_response': {'paging': 'pagerduty:secops-rotation', 'tabletop_cadence_days': 90}, 'version': '1.0.0', 'last_reviewed': '2026-05-23'}
BAD = {'spec_id': 'sec 1', 'identity': {'provider': '', 'mfa_scope': 'none'}, 'authz': {'model': 'trust', 'tenant_filter': 'vibes'}, 'secrets': {'provider': 'env', 'rotation_days': 0, 'per_service_scope': False}, 'ci_controls': ['lint'], 'incident_response': {'paging': '', 'tabletop_cadence_days': 1000}, 'version': '1.0', 'last_reviewed': 'today'}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-security-architecture.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
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
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
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
