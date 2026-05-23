#!/usr/bin/env python3
"""validate-agile-hybrid-approaches.py — F-066 B4 stdlib validator for the Agile and Hybrid Approaches artefact.

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

REQUIRED = ['adr_id', 'project_id', 'factor_scores', 'recommendation', 'decision_owner']


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


OK_FIXTURE = json.loads('{"adr_id": "ADR-2026-014", "project_id": "acme-platform-rebuild", "factor_scores": {"requirements_clarity": {"score": "H", "evidence": [{"source": "charter v2", "citation": "core stable, integrations evolving"}]}, "stakeholder_availability": {"score": "H", "evidence": [{"source": "kickoff transcript", "citation": "biweekly steering committee"}]}, "risk_tolerance": {"score": "P", "evidence": [{"source": "MSA clause 4.2", "citation": "compliance gate must pass"}]}, "team_experience": {"score": "H", "evidence": [{"source": "team-doc", "citation": "2 seniors + 2 mid + 1 junior"}]}, "contract_type": {"score": "P", "evidence": [{"source": "SoW", "citation": "fixed-price phase-1"}]}}, "recommendation": {"approach": "Hybrid", "rationale": "2 P + 3 H -> Hybrid (Water-Scrum-Fall) with fixed planning and deploy phases, agile build."}, "decision_owner": "Iryna V.", "phases": [{"name": "Discovery", "approach": "Agile", "definition_of_done": "Prototype validated with 3 stakeholders."}, {"name": "Build", "approach": "Agile", "definition_of_done": "Sprint demo accepted; tests green in CI."}, {"name": "Deploy", "approach": "Predictive", "definition_of_done": "All AC verified; staged rollout complete; docs signed."}]}')
BAD_FIXTURE = json.loads('{"adr_id": "ADR", "factor_scores": {"requirements_clarity": "P"}, "recommendation": {"approach": "Hybrid"}}')


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
