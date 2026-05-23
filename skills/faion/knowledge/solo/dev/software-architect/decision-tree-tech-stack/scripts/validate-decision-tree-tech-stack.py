#!/usr/bin/env python3
"""validate-decision-tree-tech-stack.py

Validate the artefact produced by the decision-tree-tech-stack methodology against the JSON
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

REQUIRED: tuple[str, ...] = ('adr_id', 'status', 'language', 'framework', 'datastore', 'rejected', 'rationale', 'review_trigger', 'version', 'last_reviewed',)
ENUMS: dict[str, list] = {'status': ['proposed', 'accepted', 'superseded', 'deprecated']}


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


OK = {'adr_id': 'adr-stack-chat-2026-05', 'status': 'accepted', 'language': 'python', 'framework': 'fastapi', 'datastore': 'timescaledb', 'rejected': [{'name': 'go+gin', 'reason': 'Team Python expertise dominates; real-time perf within target on Python.'}, {'name': 'node+nestjs', 'reason': 'Datastore time-series fit weaker; team less familiar.'}], 'risk_budget_weeks': 0, 'rationale': 'Team expertise concentration 75% in Python; FastAPI mature; TimescaleDB matches chat-events time-series data shape.', 'review_trigger': 'Sustained > 5k RPS OR p95 latency > 200ms for 30 consecutive days.', 'version': '1.0.0', 'last_reviewed': '2026-05-23'}
BAD = {'adr_id': 'stack 1', 'status': 'ok', 'language': '', 'framework': 'fastapi', 'datastore': 'mongo', 'rejected': [], 'rationale': 'we like it', 'review_trigger': '', 'version': '1.0', 'last_reviewed': 'today'}


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
        prog="validate-decision-tree-tech-stack.py",
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
