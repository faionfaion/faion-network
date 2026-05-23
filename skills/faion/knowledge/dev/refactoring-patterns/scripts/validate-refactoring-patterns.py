#!/usr/bin/env python3
"""validate-refactoring-patterns.py

Validate a refactor playbook JSON against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to playbook JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ALLOWED_TRANSFORMS = {
    "extract-method",
    "extract-class",
    "rename",
    "replace-conditional-with-polymorphism",
    "decompose-conditional",
    "introduce-parameter-object",
    "replace-magic-number",
    "replace-derived-variable-with-query",
    "move-method",
}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("target", "steps", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    steps = obj.get("steps")
    if not isinstance(steps, list) or not steps:
        errs.append("steps must be non-empty list")
    else:
        for i, s in enumerate(steps):
            if not isinstance(s, dict):
                errs.append(f"steps[{i}] must be object")
                continue
            for k in ("transform", "scope_files", "tests_green_before", "tests_green_after"):
                if k not in s:
                    errs.append(f"steps[{i}] missing {k}")
            if s.get("transform") and s["transform"] not in ALLOWED_TRANSFORMS:
                errs.append(f"steps[{i}].transform must be in {sorted(ALLOWED_TRANSFORMS)}")
            sf = s.get("scope_files")
            if sf is not None and (not isinstance(sf, list) or len(sf) > 5):
                errs.append(f"steps[{i}].scope_files must be list of <=5")
            if s.get("tests_green_before") is not True:
                errs.append(f"steps[{i}].tests_green_before must be true")
            if s.get("tests_green_after") is not True:
                errs.append(f"steps[{i}].tests_green_after must be true")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


OK = {
    "target": "src/x.py",
    "steps": [
        {
            "transform": "extract-method",
            "scope_files": ["src/x.py"],
            "tests_green_before": True,
            "tests_green_after": True,
        }
    ],
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "target": "src/x",
    "steps": [
        {
            "transform": "big-rewrite",
            "scope_files": ["a", "b", "c", "d", "e", "f"],
            "tests_green_before": False,
            "tests_green_after": True,
        }
    ],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("OK rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("BAD accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
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
    errs = validate(json.loads(p.read_text()))
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
