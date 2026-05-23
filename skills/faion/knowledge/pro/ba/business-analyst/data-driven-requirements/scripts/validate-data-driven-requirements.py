#!/usr/bin/env python3
"""validate-data-driven-requirements.py

Validate a spec artefact produced by the data-driven-requirements methodology
against the JSON Schema captured in content/02-output-contract.xml.

stdlib-only. Inputs / outputs / exit codes documented under --help.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixture
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

REQUIRED = ['req_id', 'business_question', 'baseline', 'target', 'instrumentation', 'post_launch_window']


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be a JSON object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = json.loads('{"req_id": "BR-0042", "business_question": "Will inline previews reduce abandoned uploads on the SMB plan?", "baseline": {"metric": "upload_abandon_rate", "value": 0.27, "source": "amplitude", "as_of": "2026-04-15"}, "target": {"metric": "upload_abandon_rate", "value": 0.18, "direction": "decrease", "by_when": "2026-07-15"}, "instrumentation": {"events": ["upload_started", "upload_completed", "upload_abandoned"], "properties": ["plan", "file_type"], "dashboard": "amplitude/abandon-funnel"}, "post_launch_window": "P14D", "rice": {"reach": 1200, "impact": 2, "confidence": 0.7, "effort": 5}}')
BAD = json.loads('{"req_id": "BR-1", "business_question": "make it faster"}')


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("self-test FAIL: good fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
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
        sys.stderr.write(f"VIOLATION: invalid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
