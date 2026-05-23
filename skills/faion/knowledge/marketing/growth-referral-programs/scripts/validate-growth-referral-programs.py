#!/usr/bin/env python3
"""validate-growth-referral-programs.py

Validates a spec artefact produced by methodology 'growth-referral-programs' against the
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

REQUIRED = ["slug", "owner", "review_deadline", "summary", "sections", "deviation_log_reference"]


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "slug" in obj and obj["slug"] != "growth-referral-programs":
        errs.append(f"slug must equal 'growth-referral-programs'")
    if "sections" in obj:
        if not isinstance(obj["sections"], list) or len(obj["sections"]) < 3:
            errs.append("sections must be array with >=3 items")
        else:
            for i, sec in enumerate(obj["sections"]):
                if not isinstance(sec, dict):
                    errs.append(f"sections[{i}] must be object")
                    continue
                for sk in ("name", "content"):
                    if sk not in sec:
                        errs.append(f"sections[{i}] missing {sk}")
    serialised = json.dumps(obj)
    for marker in ("TBD", "TODO", "FIXME"):
        if marker in serialised:
            errs.append(f"forbidden token in payload: {marker}")
    return errs


FIXTURE_OK = {"slug": "growth-referral-programs", "owner": "growth lead", "review_deadline": "2026-06-15", "summary": "Spec for test covering preconditions, procedure, output, and review gate.", "sections": [{"name": "preconditions", "content": "All Applies If items confirmed in writing."}, {"name": "procedure", "content": "Steps 1..n executed per content/04-procedure.xml."}, {"name": "review", "content": "Human reviewer signed off on date."}], "deviation_log_reference": "ops/deviation-log.md#L42", "signoff": {"reviewer": "growth lead", "date": "2026-06-10"}}


def self_test() -> int:
    errs = validate(FIXTURE_OK)
    if errs:
        for e in errs:
            sys.stderr.write(f"self-test fixture rejected: {e}\n")
        return 1
    errs2 = validate({"slug": "growth-referral-programs"})
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
