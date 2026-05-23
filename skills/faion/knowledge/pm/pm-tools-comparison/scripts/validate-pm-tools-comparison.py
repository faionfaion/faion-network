#!/usr/bin/env python3
"""validate-pm-tools-comparison.py — F-066 B4 stdlib validator for the PM Tools Comparison artefact.

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

REQUIRED = ['report_id', 'tools', 'criteria_weights', 'scores', 'tco', 'recommendation', 'decision_owner']


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


OK_FIXTURE = json.loads('{"report_id": "ptc-2026-Q2", "tools": ["jira", "linear", "clickup"], "criteria_weights": {"core_features": 0.3, "usability": 0.25, "integrations": 0.2, "enterprise": 0.15, "cost": 0.1}, "scores": {"jira": {"core_features": 4, "usability": 3, "integrations": 5, "enterprise": 5, "cost": 3, "evidence": [{"source": "PoC week 2 log", "citation": "WIQL replacement needed"}]}, "linear": {"core_features": 4, "usability": 5, "integrations": 4, "enterprise": 3, "cost": 4, "evidence": [{"source": "PoC week 2 log", "citation": "fast triage but weaker reporting"}]}, "clickup": {"core_features": 4, "usability": 3, "integrations": 4, "enterprise": 3, "cost": 4, "evidence": [{"source": "PoC week 2 log", "citation": "configurable but cluttered"}]}}, "tco": {"jira": {"year_1": 18000, "year_2": 18000, "year_3": 19000, "total": 55000}, "linear": {"year_1": 14000, "year_2": 14000, "year_3": 15000, "total": 43000}, "clickup": {"year_1": 12000, "year_2": 12000, "year_3": 13000, "total": 37000}}, "recommendation": {"tool": "linear", "rationale": "Highest weighted total (4.05) + lowest friction in PoC."}, "decision_owner": "Iryna V.", "dissents": [{"from": "Marko P.", "reason": "Prefers Jira for WIQL parity."}]}')
BAD_FIXTURE = json.loads('{"report_id": "ptc", "tools": ["jira"], "scores": {"jira": {"core_features": 4}}, "recommendation": {"tool": "linear"}}')


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
