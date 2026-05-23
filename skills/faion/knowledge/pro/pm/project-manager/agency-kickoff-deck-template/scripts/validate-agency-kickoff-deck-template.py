#!/usr/bin/env python3
"""validate-agency-kickoff-deck-template.py

Validate the artefact produced for the agency-kickoff-deck-template methodology against the schema
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

REQUIRED = ['client', 'project', 'sponsor', 'outcome', 'scope_in', 'scope_out', 'success_metrics', 'workstreams', 'milestones', 'risks', 'comms_cadence', 'decision_asks']


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"client": "ACME", "project": "checkout-redesign", "sponsor": "ACME-VP-Eng", "outcome": "p95 < 500ms in 90 days", "scope_in": ["Stripe Payment Intents v2"], "scope_out": ["Mobile app", "Loyalty"], "success_metrics": ["p95 latency", "Apple Pay conversion"], "workstreams": [{"name": "Payments", "owner_agency": "Iryna", "owner_client": "ACME-Lead-Eng"}], "milestones": [{"name": "Canary", "date": "2026-06-15"}], "risks": [{"statement": "Vendor SOW signed late", "owner": "Iryna", "trigger": "no signed SOW by 2026-05-30"}, {"statement": "Key dev PTO", "owner": "Iryna", "trigger": "PTO conflict in calendar"}, {"statement": "Latency budget overrun", "owner": "TL Petro", "trigger": "p95 > 800ms in dev env"}, {"statement": "Apple Pay device coverage", "owner": "Olena", "trigger": "iOS Safari test < 95%"}, {"statement": "JWT migration regressions", "owner": "Iryna", "trigger": "error rate > 0.5% in canary"}], "comms_cadence": {"channel": "Slack #checkout", "frequency": "weekly Mon 9am UTC", "owner": "PM Iryna"}, "decision_asks": [{"n": 1, "ask": "Approve canary geography UA+PT first"}]}')
BAD = json.loads('{"client": "x"}')


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
