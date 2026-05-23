#!/usr/bin/env python3
"""validate-agency-discovery-call-scorecard.py

Validates a rubric artefact produced by methodology 'agency-discovery-call-scorecard' against the
JSON Schema embedded in content/02-output-contract.xml.

Inputs:
    --file PATH       artefact JSON path
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["slug", "axes", "score_range", "decision_threshold", "owner"]


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "slug" in obj and obj["slug"] != "agency-discovery-call-scorecard":
        errs.append(f"slug must equal 'agency-discovery-call-scorecard'")
    if "axes" in obj and (not isinstance(obj["axes"], list) or len(obj["axes"]) < 3):
        errs.append("axes must be array with >=3 items")
    serialised = json.dumps(obj)
    for marker in ("TBD", "TODO", "FIXME"):
        if marker in serialised:
            errs.append(f"forbidden token in payload: {marker}")
    return errs


FIXTURE_OK = {"slug": "agency-discovery-call-scorecard", "axes": [{"name": "fit", "weight": 0.3, "anchors": ["poor", "good", "excellent"]}, {"name": "budget", "weight": 0.3, "anchors": ["<5k", "5-20k", ">20k"]}, {"name": "urgency", "weight": 0.2, "anchors": ["browsing", "this quarter", "this month"]}, {"name": "decision_maker", "weight": 0.2, "anchors": ["IC", "manager", "owner"]}], "score_range": [0, 100], "decision_threshold": 60, "owner": "sales lead"}


def self_test() -> int:
    errs = validate(FIXTURE_OK)
    if errs:
        for e in errs:
            sys.stderr.write(f"self-test fixture rejected: {e}\n")
        return 1
    errs2 = validate({"slug": "agency-discovery-call-scorecard"})
    if not errs2:
        sys.stderr.write("self-test: deliberately-broken fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
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
        sys.stderr.write(f"JSON parse error: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
