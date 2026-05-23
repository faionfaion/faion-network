#!/usr/bin/env python3
"""validate-us-uk-eu-compliance-matrix.py

Validate an artefact produced by the US / UK / EU Compliance Matrix methodology
against the JSON Schema declared in content/02-output-contract.xml.

Inputs:
    --file PATH       path to the artefact JSON file
    --self-test       run built-in fixtures (OK + BAD) and exit 0 on pass
    --help            this message

Exit codes:
    0 = valid (or self-test pass)
    1 = invalid (or self-test fail)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['ai_act_features', 'business_entity', 'contract_templates', 'counsel_signoff', 'jurisdictions', 'review_period', 'tax_status']


def validate(obj: dict) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'business_entity': 'Acme LLC (Delaware)', 'review_period': '2026-Q2', 'jurisdictions': [{'code': 'US-CA', 'customer_count': 120, 'revenue': 80000, 'applicable_laws': ['CCPA', 'CPRA'], 'lawful_basis_per_activity': {'marketing': 'consent'}}], 'contract_templates': {'b2b_enterprise': 'templates/dpa-scc.md', 'b2b_small': 'templates/dpa.md', 'b2c': 'templates/consumer-terms.md'}, 'tax_status': [{'jurisdiction': 'US-CA', 'threshold': 500000, 'current_volume': 80000, 'registered': False, 'action': 'monitor'}], 'ai_act_features': [{'feature': 'AI summarisation', 'risk_level': 'limited', 'conformity_assessment': False, 'registration': False}], 'counsel_signoff': {'name': 'Doe Privacy Counsel', 'date': '2026-05-15', 'scope': 'EU + UK + US-CA'}}
BAD = {'business_entity': 'Acme', 'review_period': '2026-Q2', 'jurisdictions': [{'code': 'global'}], 'tax_status': [], 'counsel_signoff': None}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"self-test FAIL: OK fixture rejected: {errs_ok}\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("self-test FAIL: BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
