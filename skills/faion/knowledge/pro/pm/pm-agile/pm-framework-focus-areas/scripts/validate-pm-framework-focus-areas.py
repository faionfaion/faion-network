#!/usr/bin/env python3
"""validate-pm-framework-focus-areas.py — F-066 B4 stdlib validator for the PM Framework Focus Areas artefact.

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

REQUIRED = ['adr_id', 'project_id', 'focus_areas', 'decision_owner', 'review_due']


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


OK_FIXTURE = json.loads('{"adr_id": "ADR-2026-027", "project_id": "orion-platform", "focus_areas": {"initiating": {"practices": [{"name": "Project charter v2", "evidence": [{"source": "charter.md", "citation": "v2 signed 2026-04-10"}]}]}, "planning": {"practices": [{"name": "Quarterly roadmap", "evidence": [{"source": "roadmap-2026-Q2.md", "citation": "5 milestones"}]}]}, "executing": {"practices": [{"name": "Sprint planning + daily standups", "evidence": [{"source": "calendar", "citation": "Mon 10:00 + daily 09:30"}]}]}, "monitoring_and_controlling": {"practices": [{"name": "Cycle-time dashboard", "evidence": [{"source": "dashboard", "citation": "p50 5d, p90 14d"}]}]}, "closing": {"practices": [{"name": "Release retros", "evidence": [{"source": "retros/W21.md", "citation": "5 actions, 4 closed"}]}]}}, "decision_owner": "Iryna V.", "review_due": "2026-08-23"}')
BAD_FIXTURE = json.loads('{"adr_id": "ADR", "focus_areas": {"planning": {"practices": ["plan"]}}, "decision_owner": ""}')


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
