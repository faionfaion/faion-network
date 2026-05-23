#!/usr/bin/env python3
"""validate-php-phpunit-testing.py

Validate the test-plan manifest for the php-phpunit-testing methodology against
the JSON Schema declared in 02-output-contract.xml.

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
import sys
from pathlib import Path

REQUIRED = ["framework", "test_dbms", "test_classes", "coverage_min", "gate_enforced_in_ci"]
FRAMEWORKS = {"pest", "phpunit"}
DBMS = {"postgres", "mysql", "sqlite"}
LAYERS = {"feature", "unit"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("framework") not in FRAMEWORKS:
        errs.append(f"framework must be one of {sorted(FRAMEWORKS)}")
    if obj.get("test_dbms") not in DBMS:
        errs.append(f"test_dbms must be one of {sorted(DBMS)}")
    classes = obj.get("test_classes") or []
    if not isinstance(classes, list) or len(classes) < 1:
        errs.append("test_classes must be non-empty list")
    for i, c in enumerate(classes):
        if c.get("layer") not in LAYERS:
            errs.append(f"test_classes[{i}].layer must be one of {sorted(LAYERS)}")
        if c.get("layer") == "feature" and c.get("uses_refresh_database") is not True:
            errs.append(f"test_classes[{i}] feature must use RefreshDatabase")
    if not isinstance(obj.get("coverage_min"), int) or obj.get("coverage_min", 0) < 80:
        errs.append("coverage_min must be int >= 80")
    if obj.get("gate_enforced_in_ci") is not True:
        errs.append("gate_enforced_in_ci must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "framework": "pest",
    "test_dbms": "postgres",
    "test_classes": [
        {"name": "Tests\\Feature\\Api\\UserCreateTest", "layer": "feature", "uses_refresh_database": True},
        {"name": "Tests\\Unit\\Services\\InvoiceCalculatorTest", "layer": "unit", "uses_refresh_database": False},
    ],
    "coverage_min": 82,
    "gate_enforced_in_ci": True,
    "forbidden_patterns_found": [],
}
BAD = {
    "framework": "codeception",
    "test_dbms": "redis",
    "test_classes": [{"name": "FeatureUserTest", "layer": "feature", "uses_refresh_database": False}],
    "coverage_min": 40,
    "gate_enforced_in_ci": False,
    "forbidden_patterns_found": ["Mail::fake() after action"],
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
