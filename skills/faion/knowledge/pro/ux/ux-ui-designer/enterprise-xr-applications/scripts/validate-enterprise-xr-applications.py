#!/usr/bin/env python3
"""validate-enterprise-xr-applications.py

Validate Enterprise XR Applications artefact JSON against the schema in 02-output-contract.xml.

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

REQUIRED = ['use_case', 'headset_coverage_pct', 'comfort_budget', 'it_integration', 'security_review', 'roi']


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    return errs


OK = {'use_case': 'training-simulation', 'headset_coverage_pct': 72, 'comfort_budget': {'max_continuous_minutes': 25, 'break_cadence_minutes': 5, 'vestibular_safe': True}, 'it_integration': {'sso': 'Okta SAML', 'mdm': 'Intune'}, 'security_review': {'spatial_data_privacy': 'room-scan retained 30d', 'recording_governance': 'session recordings encrypted at rest + 90d retention'}, 'roi': {'baseline': '$12k/hr machine downtime training', 'target': '30% reduction in time-to-competence', 'measurement': 'pre/post assessment + downtime tracking'}}
BAD = {'use_case': 'training-simulation'}


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
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
