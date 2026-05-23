#!/usr/bin/env python3
"""validate-hybrid-delivery.py — F-066 B4 stdlib validator for the Hybrid Delivery artefact.

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

REQUIRED = ['adr_id', 'program_id', 'components', 'translation_boundaries', 'governance_cadence']


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


OK_FIXTURE = json.loads('{"adr_id": "ADR-2026-021", "program_id": "orion-platform", "components": [{"name": "Compliance certification", "method": "Predictive", "risk_profile": "compliance", "evidence": [{"source": "ISO-27001 plan", "citation": "audit gate at M9"}]}, {"name": "Customer dashboard", "method": "Agile", "risk_profile": "low-risk-iterative", "evidence": [{"source": "UX brief", "citation": "weekly feedback loop with pilot customers"}]}], "translation_boundaries": [{"from_component": "Customer dashboard", "to_component": "Compliance certification", "artefact": "Audit log spec", "contract": "Sprint-22 demo accepted -> audit-log spec frozen for certification."}], "governance_cadence": {"stage_gates": [{"name": "Gate 1: Design", "due": "2026-06-30"}, {"name": "Gate 2: Pilot", "due": "2026-09-30"}, {"name": "Gate 3: Cert", "due": "2026-12-15"}]}}')
BAD_FIXTURE = json.loads('{"adr_id": "ADR", "program_id": "orion", "components": [{"name": "Dashboard", "method": "Agile"}], "translation_boundaries": []}')


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
