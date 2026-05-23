#!/usr/bin/env python3
"""validate-accessibility-automation-qa.py

Validate the artefact for accessibility-automation-qa against the schema in content/02-output-contract.xml.

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

REQUIRED = ['steps', 'decision_branches', 'owner_of_playbook', 'deviation_log_reference', 'wcag_floor']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK_FIXTURE = '{"steps": [{"id": "S1", "input": "signup flow", "owner": "bob", "exit_criterion": "axe-core blocking=0", "output_location": "tests/a11y/signup.spec.ts"}, {"id": "S2", "input": "checkout flow", "owner": "bob", "exit_criterion": "axe-core blocking=0", "output_location": "tests/a11y/checkout.spec.ts"}, {"id": "S3", "input": "search flow", "owner": "bob", "exit_criterion": "axe-core blocking=0", "output_location": "tests/a11y/search.spec.ts"}, {"id": "S4", "input": "dashboard", "owner": "bob", "exit_criterion": "Lighthouse a11y \\u226595", "output_location": "tests/a11y/dashboard.spec.ts"}], "decision_branches": [{"id": "DB1", "signal": "axe-core rule color-contrast severity=critical", "if_true": "block PR", "if_false": "ticket"}], "owner_of_playbook": "bob@co", "deviation_log_reference": "docs/a11y/deviations.md", "wcag_floor": "2.1-AA"}'
BAD_FIXTURE = '{"steps": [{"id": "S1"}], "decision_branches": [], "owner_of_playbook": "", "wcag_floor": "2.0"}'


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
