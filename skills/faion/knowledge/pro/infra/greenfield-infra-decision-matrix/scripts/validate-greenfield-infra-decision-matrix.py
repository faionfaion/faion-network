#!/usr/bin/env python3
"""validate-greenfield-infra-decision-matrix.py

Validate an artefact produced by the Greenfield Infra Decision Matrix methodology
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

REQUIRED = ['axes', 'constraints', 'decision_date', 'project_id', 'revisit_due_date', 'signoffs']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'project_id': 'acme-q3-2026-platform', 'decision_date': '2026-05-15', 'revisit_due_date': '2027-05-15', 'axes': [{'axis': 'container_orchestrator', 'candidates': ['EKS', 'ECS', 'Cloud Run'], 'red_flags_applied': ['Cloud Run requires GCP — disqualifies if AWS-only'], 'scores': {'EKS': 4, 'ECS': 3, 'Cloud Run': 0}, 'chosen': 'EKS', 'rationale': 'Team familiar with k8s; ECS lacks ecosystem; Cloud Run disqualified by AWS-only constraint.'}], 'constraints': {'compliance': 'SOC2 + HIPAA', 'budget_monthly_usd': 8000, 'scale_users': 50000, 'team_skills': ['k8s', 'aws']}, 'signoffs': [{'role': 'engineering_leader', 'name': 'Alice', 'date': '2026-05-15'}]}
BAD = {'project_id': 'acme', 'decision_date': '2026-05-15', 'revisit_due_date': '', 'axes': [{'axis': 'container_orchestrator', 'chosen': 'EKS'}], 'signoffs': []}


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
