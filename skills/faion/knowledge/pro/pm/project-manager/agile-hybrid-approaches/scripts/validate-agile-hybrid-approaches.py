#!/usr/bin/env python3
"""validate-agile-hybrid-approaches.py

Validate the artefact produced for the agile-hybrid-approaches methodology against the schema
in content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['programme', 'decision_date', 'sponsor', 'dimensions', 'recommendation', 'named_hybrid_tilt', 'reevaluation_triggers']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"programme": "regulated-claims-platform", "decision_date": "2026-05-22", "sponsor": "COO", "dimensions": {"requirement_volatility": {"score": 0.4, "evidence": "regulator change-log cadence"}, "team_skill_uniformity": {"score": 0.6, "evidence": "skill-matrix Q2"}, "failure_cost_low": {"score": 0.2, "evidence": "SLA fines $200k per outage"}, "team_size_small": {"score": 0.5, "evidence": "8 FTE delivery team"}, "culture_fit_agile": {"score": 0.7, "evidence": "team Scrum maturity score 4/5"}, "domain_uncertainty_high": {"score": 0.5, "evidence": "BA discovery notes Q1"}}, "recommendation": "hybrid", "named_hybrid_tilt": "predictive on regulatory milestones + audit gates; agile on UX + reporting layer", "reevaluation_triggers": ["velocity volatility > 30% over 3 sprints", "escalation rate > 1 per sprint for 2 sprints"]}')
BAD = json.loads('{"programme": "x", "decision_date": "2026-05-22", "sponsor": "x"}')


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: OK fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON path")
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
