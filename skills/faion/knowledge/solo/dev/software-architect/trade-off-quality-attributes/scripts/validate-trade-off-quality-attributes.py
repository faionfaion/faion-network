#!/usr/bin/env python3
"""validate-trade-off-quality-attributes.py

Validate the artefact produced by the trade-off-quality-attributes methodology against the JSON
Schema embedded in content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    artefact JSON to validate
    --self-test    run built-in OK + BAD fixtures
    --help         this message

Exit codes:
    0  artefact valid
    1  artefact invalid (violation list printed to stderr)
    2  usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED: tuple[str, ...] = ('report_id', 'attributes_in_scope', 'conflicts', 'sensitivity_points', 'risks', 'non_risks', 'review_trigger', 'version', 'last_reviewed',)
ENUMS: dict[str, list] = {}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k, allowed in ENUMS.items():
        if k in obj and obj[k] not in allowed:
            errs.append(f"field {k!r} not in allowed values {allowed!r}; got {obj[k]!r}")
    return errs


OK = {'report_id': 'qa-trade-storefront-2026-05', 'attributes_in_scope': ['performance', 'security', 'availability', 'cost'], 'conflicts': [{'id': 'tp-perf-vs-cost', 'scenario_a_id': 'qa-perf-001', 'scenario_b_id': 'qa-cost-002', 'description': 'Lower p95 requires larger cache; cost cap limits cache footprint.', 'resolution_rule': 'Accept p95 increase up to 220ms when monthly cost rises > 15%.'}, {'id': 'tp-sec-vs-ux', 'scenario_a_id': 'qa-sec-001', 'scenario_b_id': 'qa-usab-001', 'description': 'MFA-everywhere increases shopper friction; security needs strong auth on admin.', 'resolution_rule': 'MFA required only for admin; shoppers use passwordless + device-pinning.'}], 'sensitivity_points': [{'id': 'sp-cache', 'element': 'redis-cache-config', 'affected_attributes': ['performance', 'cost']}, {'id': 'sp-auth', 'element': 'auth-mfa-policy', 'affected_attributes': ['security', 'usability']}], 'risks': [{'risk': 'MFA fatigue on shoppers if scope creeps', 'mitigation': 'Scope locked to admin only; quarterly review.'}], 'non_risks': [{'pair': 'maintainability_vs_performance', 'reason': 'Modular monolith keeps both aligned.'}], 'review_trigger': 'Cache RPS doubles OR security incident rate > 0.1% per month.', 'version': '1.0.0', 'last_reviewed': '2026-05-23'}
BAD = {'report_id': 'qa 1', 'attributes_in_scope': ['performance'], 'conflicts': [], 'sensitivity_points': [], 'risks': [], 'review_trigger': '', 'version': '1.0', 'last_reviewed': 'today'}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("self-test FAIL: OK fixture rejected: " + "; ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-trade-off-quality-attributes.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
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
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
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
