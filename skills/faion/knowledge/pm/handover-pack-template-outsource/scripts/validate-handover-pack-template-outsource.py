#!/usr/bin/env python3
"""validate-handover-pack-template-outsource.py — F-066 B4 stdlib validator for the Handover Pack Template Outsource artefact.

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

REQUIRED = ['pack_id', 'engagement_id', 'outgoing_specialist', 'receiving_owner', 'decisions_log', 'open_issues', 'runbooks', 'contacts', 'acceptance_gate']


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


OK_FIXTURE = json.loads('{"pack_id": "hp-2026-acme-001", "engagement_id": "acme-platform-rebuild", "outgoing_specialist": {"name": "Olena K.", "contact": "olena@example.com"}, "receiving_owner": {"name": "Marko P.", "contact": "marko@acme.example"}, "decisions_log": [{"title": "Use Postgres for events", "decided_on": "2026-03-04", "source": "ADR-007 / PR#1142", "rationale": "Avoid Kafka ops overhead at <1k events/s."}], "open_issues": [{"title": "Migration script flaky on staging", "owner_after_handover": "Marko P.", "expected_by": "2026-06-07"}], "runbooks": [{"name": "Rotate DB credentials", "last_executed_on": "2026-05-02"}], "contacts": [{"name": "Iryna V.", "role": "DevOps lead", "last_contacted": "2026-05-10"}], "acceptance_gate": {"status": "pending"}}')
BAD_FIXTURE = json.loads('{"pack_id": "hp", "engagement_id": "?", "decisions_log": [{"title": "Use Postgres"}], "open_issues": [{"title": "Migration flaky"}], "acceptance_gate": {"status": "acknowledged"}}')


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
