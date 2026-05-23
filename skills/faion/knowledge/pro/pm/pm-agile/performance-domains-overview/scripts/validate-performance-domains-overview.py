#!/usr/bin/env python3
"""validate-performance-domains-overview.py — F-066 B4 stdlib validator for the Performance Domains Overview artefact.

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

REQUIRED = ['report_id', 'project_id', 'assessor', 'domains', 'remediations']


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


OK_FIXTURE = json.loads('{"report_id": "pdo-2026-Q2-orion", "project_id": "orion-platform", "assessor": "Iryna V.", "domains": {"stakeholder": {"score": 4, "evidence": [{"source": "status report W18", "citation": "stakeholder map up to date"}, {"source": "retro W20", "citation": "stakeholder feedback loop biweekly"}]}, "team": {"score": 3, "evidence": [{"source": "team-doc", "citation": "2 seniors + 2 mid + 1 junior"}, {"source": "1:1 notes W19", "citation": "junior onboarding paired well"}]}, "development_approach": {"score": 4, "evidence": [{"source": "ADR-014", "citation": "Hybrid Water-Scrum-Fall"}, {"source": "demo W20", "citation": "sprint cadence stable"}]}, "planning": {"score": 2, "evidence": [{"source": "plan v3", "citation": "plan v3 not refreshed since W12"}, {"source": "retro W20", "citation": "plan drift flagged"}]}, "project_work": {"score": 3, "evidence": [{"source": "cycle-time chart W18-W21", "citation": "p50 5d stable"}, {"source": "WIP chart", "citation": "WIP 6 within limit 8"}]}, "delivery": {"score": 4, "evidence": [{"source": "release-W21", "citation": "shipped within scope"}, {"source": "customer feedback", "citation": "NPS +12"}]}, "measurement": {"score": 3, "evidence": [{"source": "metrics dashboard", "citation": "lead/cycle/throughput live"}, {"source": "risk register", "citation": "monthly review cadence"}]}, "uncertainty": {"score": 2, "evidence": [{"source": "risk register", "citation": "3 of 7 risks stale >60d"}, {"source": "retro W18", "citation": "unmodelled compliance risk"}]}}, "remediations": [{"domain": "planning", "action": "Refresh plan v4 with revised milestones", "owner": "Iryna V.", "due": "2026-06-07"}, {"domain": "uncertainty", "action": "Risk register refresh + compliance risk modelling", "owner": "Marko P.", "due": "2026-06-14"}]}')
BAD_FIXTURE = json.loads('{"report_id": "pdo", "domains": {"stakeholder": {"score": 4}}, "remediations": []}')


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
