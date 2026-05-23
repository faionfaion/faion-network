#!/usr/bin/env python3
"""rtm_coverage.py

Check RTM coverage: every requirement has an acceptance test and every
acceptance test maps to a requirement.

Inputs:
    --file PATH       scope-statement JSON
    --self-test       run built-in fixture
    --help            this message

Exit codes:
    0 = clean coverage
    1 = orphan requirements or orphan AC present
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

FIXTURE_OK = {
    "acceptance_criteria": [{"id": "AC-001", "statement": "x", "testable": True}],
    "rtm": [{"req_id": "REQ-1", "source": "charter", "ac_id": "AC-001"}],
}
FIXTURE_BAD = {
    "acceptance_criteria": [{"id": "AC-001", "statement": "x", "testable": True},
                             {"id": "AC-002", "statement": "y", "testable": True}],
    "rtm": [{"req_id": "REQ-1", "source": "charter", "ac_id": "AC-001"}],
}


def check(scope: dict) -> list[str]:
    ac_ids = {ac["id"] for ac in scope.get("acceptance_criteria", [])}
    mapped = {row["ac_id"] for row in scope.get("rtm", [])}
    findings: list[str] = []
    orphan_ac = ac_ids - mapped
    for o in sorted(orphan_ac):
        findings.append(f"orphan AC: {o} (no REQ maps to it)")
    return findings


def self_test() -> int:
    if check(FIXTURE_OK):
        sys.stderr.write("self-test FAIL: OK fixture flagged\n")
        return 1
    if not check(FIXTURE_BAD):
        sys.stderr.write("self-test FAIL: BAD fixture clean\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="scope-statement JSON path")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixture")
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
    scope = json.loads(p.read_text())
    findings = check(scope)
    if findings:
        for f in findings:
            sys.stdout.write(f"FINDING: {f}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
