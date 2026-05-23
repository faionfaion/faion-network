#!/usr/bin/env python3
"""validate-abuse-case-test-cookbook.py

Validate the artefact for abuse-case-test-cookbook against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (rc=0 if both pass)
    --help            this message

Exit codes:
    0 = valid (or self-test passed)
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['steps', 'decision_branches', 'owner_of_playbook', 'deviation_log_reference']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK_FIXTURE = '{"steps": [{"id": "S1", "input": "endpoint /api/users/:id", "owner": "alice", "exit_criterion": "IDOR test passes for tenant-isolation negative case", "output_location": "tests/security/idor_test.py"}, {"id": "S2", "input": "endpoint /api/fetch", "owner": "alice", "exit_criterion": "SSRF test denies private IP ranges", "output_location": "tests/security/ssrf_test.py"}, {"id": "S3", "input": "endpoint /api/state-change", "owner": "alice", "exit_criterion": "CSRF token enforced", "output_location": "tests/security/csrf_test.py"}, {"id": "S4", "input": "JWT misuse", "owner": "alice", "exit_criterion": "expired token rejected", "output_location": "tests/security/jwt_test.py"}], "decision_branches": [{"id": "DB1", "signal": "endpoint returns 200 for cross-tenant id", "if_true": "fail r1", "if_false": "pass"}], "owner_of_playbook": "alice@co", "deviation_log_reference": "docs/security/deviations.md"}'
BAD_FIXTURE = '{"steps": [{"id": "S1"}], "decision_branches": [], "owner_of_playbook": ""}'


def self_test() -> int:
    """Built-in fixtures: OK_FIXTURE accepted, BAD_FIXTURE rejected."""
    if validate(json.loads(OK_FIXTURE)):
        sys.stderr.write("self-test FAIL: valid fixture rejected\n")
        return 1
    if not validate(json.loads(BAD_FIXTURE)):
        sys.stderr.write("self-test FAIL: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
