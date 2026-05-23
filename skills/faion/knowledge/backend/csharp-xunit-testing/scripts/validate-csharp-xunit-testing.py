#!/usr/bin/env python3
"""validate-csharp-xunit-testing.py

Validate the test-plan manifest for the csharp-xunit-testing methodology against
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

REQUIRED = [
    "test_project",
    "framework",
    "test_classes",
    "coverage",
    "uses_testcontainers",
    "uses_webapplicationfactory",
]
ALLOWED_LAYERS = {"unit", "integration", "data"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not str(obj.get("test_project", "")).endswith("Tests"):
        errs.append("test_project must end with 'Tests'")
    if obj.get("framework") != "xunit":
        errs.append("framework must be 'xunit'")
    classes = obj.get("test_classes") or []
    if not isinstance(classes, list) or len(classes) < 1:
        errs.append("test_classes must be non-empty list")
    for i, c in enumerate(classes):
        if c.get("layer") not in ALLOWED_LAYERS:
            errs.append(f"test_classes[{i}].layer must be one of {sorted(ALLOWED_LAYERS)}")
        if not str(c.get("name", "")).endswith("Tests"):
            errs.append(f"test_classes[{i}].name must end with 'Tests'")
        if not isinstance(c.get("fact_count"), int) or c.get("fact_count", 0) < 1:
            errs.append(f"test_classes[{i}].fact_count must be a positive integer")
    cov = obj.get("coverage") or {}
    if not isinstance(cov.get("line"), (int, float)) or cov.get("line", 0) < 70:
        errs.append("coverage.line must be >= 70")
    if not isinstance(cov.get("branch"), (int, float)) or cov.get("branch", 0) < 60:
        errs.append("coverage.branch must be >= 60")
    if cov.get("gate_enforced_in_ci") is not True:
        errs.append("coverage.gate_enforced_in_ci must be true")
    if obj.get("uses_testcontainers") is not True:
        errs.append("uses_testcontainers must be true")
    if obj.get("uses_webapplicationfactory") is not True:
        errs.append("uses_webapplicationfactory must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "test_project": "Billing.Tests",
    "framework": "xunit",
    "test_classes": [
        {"name": "InvoiceServiceTests", "layer": "unit", "fact_count": 12},
        {"name": "InvoicesApiTests", "layer": "integration", "fact_count": 8},
        {"name": "InvoiceRepositoryTests", "layer": "data", "fact_count": 5},
    ],
    "coverage": {"line": 78.4, "branch": 65.2, "gate_enforced_in_ci": True},
    "uses_testcontainers": True,
    "uses_webapplicationfactory": True,
    "forbidden_patterns_found": [],
}
BAD = {
    "test_project": "billing-tests",
    "framework": "nunit",
    "test_classes": [],
    "coverage": {"line": 42.0, "branch": 31.0, "gate_enforced_in_ci": False},
    "uses_testcontainers": False,
    "uses_webapplicationfactory": False,
    "forbidden_patterns_found": ["Thread.Sleep"],
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
