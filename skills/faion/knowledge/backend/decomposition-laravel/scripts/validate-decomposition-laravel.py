#!/usr/bin/env python3
"""validate-decomposition-laravel.py

Validate the structural-lint manifest for the decomposition-laravel methodology
against the JSON Schema declared in 02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures
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

REQUIRED = [
    "php_version",
    "actions",
    "controllers",
    "namespace_whitelist_passed",
    "file_size_budgets",
]
PHP_RE = re.compile(r"^8\.(1|2|3|4)")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not PHP_RE.match(str(obj.get("php_version", ""))):
        errs.append("php_version must be 8.1, 8.2, 8.3, or 8.4")
    actions = obj.get("actions") or []
    if not isinstance(actions, list) or len(actions) < 1:
        errs.append("actions must be non-empty list")
    for i, a in enumerate(actions):
        if not str(a.get("class", "")).endswith("Action"):
            errs.append(f"actions[{i}].class must end with 'Action'")
        if a.get("returns") == "void":
            errs.append(f"actions[{i}].returns must not be void")
    for i, c in enumerate(obj.get("controllers") or []):
        if not str(c.get("class", "")).endswith("Controller"):
            errs.append(f"controllers[{i}].class must end with 'Controller'")
        if not isinstance(c.get("loc"), int) or c.get("loc", 0) > 150:
            errs.append(f"controllers[{i}].loc must be <= 150")
    if obj.get("namespace_whitelist_passed") is not True:
        errs.append("namespace_whitelist_passed must be true")
    b = obj.get("file_size_budgets") or {}
    if b.get("controller_max", 999) > 150:
        errs.append("file_size_budgets.controller_max must be <= 150")
    if b.get("action_max", 999) > 100:
        errs.append("file_size_budgets.action_max must be <= 100")
    if b.get("dto_max", 999) > 40:
        errs.append("file_size_budgets.dto_max must be <= 40")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "php_version": "8.2",
    "actions": [
        {"class": "App\\Actions\\CreateUserAction", "verb": "create", "returns": "App\\Models\\User"}
    ],
    "controllers": [{"class": "App\\Http\\Controllers\\UserController", "loc": 88}],
    "namespace_whitelist_passed": True,
    "file_size_budgets": {"controller_max": 142, "action_max": 76, "dto_max": 32},
    "forbidden_patterns_found": [],
}
BAD = {
    "php_version": "7.4",
    "actions": [{"class": "UserManager", "verb": "manage", "returns": "void"}],
    "controllers": [{"class": "App\\Http\\Controllers\\UserController", "loc": 412}],
    "namespace_whitelist_passed": False,
    "file_size_budgets": {"controller_max": 412, "action_max": 230, "dto_max": 88},
    "forbidden_patterns_found": ["App\\Managers"],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
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
        sys.stderr.write(f"invalid JSON: {e}\n")
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
