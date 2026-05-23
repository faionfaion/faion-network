#!/usr/bin/env python3
"""validate-best-practices-2026.py

Validate the artefact produced by the best-practices-2026 methodology against the JSON
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

REQUIRED: tuple[str, ...] = ('repo', 'items',)
ENUMS: dict[str, list] = {}


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


OK = {'repo': 'acme/web', 'rubric_version': '2026.1', 'items': [{'id': 'ts-strict', 'status': 'PASS', 'weight': 3, 'evidence': 'tsconfig.json:12'}, {'id': 'react-19-suspense', 'status': 'WARN', 'weight': 2, 'evidence': '3 of 7 server components', 'remediation': 'wrap fetches in <Suspense>'}, {'id': 'py-3-13-strict', 'status': 'FAIL', 'weight': 3, 'evidence': 'mypy 18 errors', 'remediation': 'fix or per-module ignores'}, {'id': 'uv-or-poetry', 'status': 'PASS', 'weight': 2, 'evidence': 'pyproject.toml + uv.lock'}, {'id': 'pre-commit', 'status': 'PASS', 'weight': 2, 'evidence': '.pre-commit-config.yaml'}, {'id': 'sdd-aidocs', 'status': 'FAIL', 'weight': 1, 'evidence': 'no .aidocs/', 'remediation': 'scaffold .aidocs/'}]}
BAD = {'items': [{'id': 'x', 'status': 'ok'}]}


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
        prog="validate-best-practices-2026.py",
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
