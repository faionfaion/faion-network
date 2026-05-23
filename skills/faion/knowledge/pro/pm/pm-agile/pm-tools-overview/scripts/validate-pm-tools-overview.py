#!/usr/bin/env python3
"""validate-pm-tools-overview.py — F-066 B4 stdlib validator for the PM Tools Overview artefact.

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

REQUIRED = ['report_id', 'requirements', 'candidates', 'fit_gap', 'shortlist', 'decision_owner']


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


OK_FIXTURE = json.loads('{"report_id": "pto-2026-Q2", "requirements": [{"title": "Sprint planning + capacity tracking", "moscow": "Must", "evidence": [{"source": "retro W18", "citation": "lost capacity due to manual sprint math"}]}, {"title": "GitHub integration", "moscow": "Must", "evidence": [{"source": "support tickets", "citation": "20% of PR comments link to tracker"}]}, {"title": "Time tracking", "moscow": "Should", "evidence": [{"source": "billing pain", "citation": "hours pulled from notes weekly"}]}, {"title": "Custom dashboards", "moscow": "Could", "evidence": [{"source": "stakeholder asks", "citation": "exec wants weekly snapshot"}]}, {"title": "On-prem deployment", "moscow": "Won\'t", "evidence": [{"source": "infra ADR-009", "citation": "SaaS-first policy"}]}], "candidates": [{"name": "jira", "reason": "Industry default; PMO familiarity."}, {"name": "linear", "reason": "Fast triage UX."}, {"name": "clickup", "reason": "Configurable + low cost."}, {"name": "asana", "reason": "Cross-functional friendly."}], "fit_gap": {"jira": {"sprint_planning": "fit", "github_integration": "fit"}, "linear": {"sprint_planning": "fit", "github_integration": "fit"}, "clickup": {"sprint_planning": "partial", "github_integration": "fit"}, "asana": {"sprint_planning": "gap", "github_integration": "partial"}}, "shortlist": ["jira", "linear", "clickup"], "decision_owner": "Iryna V."}')
BAD_FIXTURE = json.loads('{"report_id": "pto", "requirements": [{"title": "good"}], "candidates": [], "shortlist": []}')


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
