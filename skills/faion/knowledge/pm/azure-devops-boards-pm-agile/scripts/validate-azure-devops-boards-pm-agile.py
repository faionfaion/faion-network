#!/usr/bin/env python3
"""validate-azure-devops-boards.py — F-066 B4 stdlib validator for the Azure DevOps Boards artefact.

Validates that an input JSON file satisfies the required-keys subset of the
schema declared in content/02-output-contract.xml of this methodology.

Inputs:
    --file PATH       path to artefact JSON file
    --self-test       run built-in pass/fail fixtures
    --help            show this message

Exit codes:
    0 — valid
    1 — invalid (violations printed to stderr)
    2 — usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['project_id', 'process_template', 'area_paths', 'iteration_paths', 'boards']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
        elif obj[k] is None:
            errs.append(f"required field is null: {k}")
    return errs


OK_FIXTURE = json.loads('{"project_id": "Acme-Platform", "process_template": "Scrum", "area_paths": ["Acme-Platform\\\\Frontend", "Acme-Platform\\\\Backend", "Acme-Platform\\\\Infra"], "iteration_paths": ["Acme-Platform\\\\2026\\\\Q2\\\\Sprint-21", "Acme-Platform\\\\2026\\\\Q2\\\\Sprint-22"], "boards": [{"team": "Frontend", "columns": [{"name": "New", "state": "New"}, {"name": "Approved", "state": "Approved"}, {"name": "Committed", "state": "Committed"}, {"name": "Done", "state": "Done"}], "swimlanes": ["Customer-Reported", "Tech-Debt"]}], "shared_queries": [{"path": "/Shared Queries/v2/active-bugs-2026-Q2", "wiql": "SELECT [System.Id] FROM workitems WHERE [System.WorkItemType]=\'Bug\' AND [System.State]<>\'Done\'"}]}')
BAD_FIXTURE = json.loads('{"project_id": "Acme", "process_template": "Custom", "area_paths": [], "boards": [{"team": "Frontend", "columns": [{"name": "Doing"}]}]}')


def self_test() -> int:
    errs = validate(OK_FIXTURE)
    if errs:
        sys.stderr.write("self-test: valid fixture rejected — " + "; ".join(errs) + "\n")
        return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("self-test: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
        obj = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"json parse error: {e}\n")
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
