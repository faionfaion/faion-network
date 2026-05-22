#!/usr/bin/env python3
"""validate-python-type-hints.py

Validate a typed-module spec JSON against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to JSON spec to validate
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALLOWED_MODES = {"greenfield", "legacy", "library"}
ALLOWED_CHECKERS = {"mypy", "pyright"}
ALLOWED_IGNORE_POLICY = {"coded-only", "any"}
PY_VER_RE = re.compile(r"^3\.(9|1[0-9])$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    required = ["python_version", "mode", "strict_files", "checker", "version", "last_reviewed"]
    for k in required:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "python_version" in obj and not PY_VER_RE.match(str(obj["python_version"])):
        errs.append("python_version must match ^3\\.(9|1[0-9])$")
    if "mode" in obj and obj["mode"] not in ALLOWED_MODES:
        errs.append(f"mode must be in {sorted(ALLOWED_MODES)}")
    if "checker" in obj and obj["checker"] not in ALLOWED_CHECKERS:
        errs.append(f"checker must be in {sorted(ALLOWED_CHECKERS)}")
    sf = obj.get("strict_files")
    if sf is not None and not isinstance(sf, list):
        errs.append("strict_files must be list")
    elif isinstance(sf, list):
        for i, v in enumerate(sf):
            if not isinstance(v, str):
                errs.append(f"strict_files[{i}] must be string")
    ip = obj.get("ignore_policy", "coded-only")
    if ip not in ALLOWED_IGNORE_POLICY:
        errs.append(f"ignore_policy must be in {sorted(ALLOWED_IGNORE_POLICY)}")
    if ip == "any":
        errs.append("ignore_policy must be coded-only — this methodology forbids bare ignores")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


OK = {
    "python_version": "3.12",
    "mode": "legacy",
    "checker": "mypy",
    "strict_files": ["src/api/handlers.py"],
    "test_relax": True,
    "ignore_policy": "coded-only",
    "future_annotations_pydantic_v2_only": True,
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "python_version": "3.8",
    "mode": "strict-everywhere",
    "checker": "mypy",
    "ignore_policy": "any",
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("OK fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("BAD fixture accepted\n")
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
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
