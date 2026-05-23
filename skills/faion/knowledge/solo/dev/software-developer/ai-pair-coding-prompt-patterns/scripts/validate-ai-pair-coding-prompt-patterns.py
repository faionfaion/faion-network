#!/usr/bin/env python3
"""validate-ai-pair-coding-prompt-patterns.py

Validate the ai-pair-coding-prompt-patterns artefact against the schema declared in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (OK + BAD)
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ('scaffold_id', 'pattern', 'task_summary', 'stop_conditions', 'acceptance_checklist', 'unit')


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    pattern = obj.get("pattern")
    valid_patterns = {"spec-first", "test-first", "repo-grep", "diff-review", "refactor-isolate", "plan-then-execute", "branch-canary"}
    if pattern not in valid_patterns:
        errs.append(f"pattern must be one of 7 named values: got {pattern!r}")
    sc = obj.get("stop_conditions") or []
    if not (isinstance(sc, list) and len(sc) >= 1):
        errs.append("stop_conditions must be non-empty list")
    cl = obj.get("acceptance_checklist") or []
    if not (isinstance(cl, list) and len(cl) >= 3):
        errs.append("acceptance_checklist must have >=3 items")
    return errs


def _load_smoke():
    p = Path(__file__).resolve().parent.parent / "templates" / "_smoke-test.json"
    obj = json.loads(p.read_text())
    obj.pop("__faion_header__", None)
    return obj


def self_test() -> int:
    ok = _load_smoke()
    errs_ok = validate(ok)
    if errs_ok:
        sys.stderr.write(f"OK fixture rejected: {errs_ok}\n")
        return 1
    bad = {}
    if not validate(bad):
        sys.stderr.write("empty BAD fixture accepted\n")
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
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"cannot parse JSON: {e}\n")
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
