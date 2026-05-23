#!/usr/bin/env python3
"""validate-csharp-xunit-testing.py

Validate a test-class spec against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       artefact JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 valid · 1 invalid · 2 usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["test_class", "scope", "all_async_return_task", "uses_fluent_assertions", "methods"]
CLASS_RE = re.compile(r"^[A-Z][A-Za-z0-9]+Tests$")
METHOD_RE = re.compile(r"^[A-Z][A-Za-z0-9]+_[A-Z][A-Za-z0-9]+_[A-Z][A-Za-z0-9]+$")
SCOPES = {"unit", "slice", "integration"}
FIXTURES = {"none", "class", "collection", "async-lifetime"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "test_class" in obj and not CLASS_RE.match(str(obj["test_class"])):
        errs.append("test_class must end with 'Tests'")
    if obj.get("scope") not in SCOPES:
        errs.append(f"scope must be one of {sorted(SCOPES)}")
    if obj.get("fixture") and obj["fixture"] not in FIXTURES:
        errs.append(f"fixture must be one of {sorted(FIXTURES)}")
    if obj.get("scope") == "integration" and obj.get("fixture") in (None, "none"):
        errs.append("integration scope requires fixture != 'none'")
    if obj.get("all_async_return_task") is not True:
        errs.append("all_async_return_task must be true")
    if obj.get("uses_fluent_assertions") is not True:
        errs.append("uses_fluent_assertions must be true")
    methods = obj.get("methods") or []
    if not methods:
        errs.append("methods must contain at least 1 entry")
    for m in methods:
        if not METHOD_RE.match(str(m.get("name", ""))):
            errs.append(f"method name '{m.get('name')}' must match Method_Input_Expected")
        if m.get("kind") not in ("Fact", "Theory"):
            errs.append(f"method.kind '{m.get('kind')}' must be Fact or Theory")
        if m.get("returns") and m["returns"] != "Task":
            errs.append(f"method '{m.get('name')}' must return Task (async-task-return)")
    return errs


OK = {
    "test_class": "OrdersControllerTests",
    "scope": "integration",
    "fixture": "class",
    "all_async_return_task": True,
    "uses_fluent_assertions": True,
    "uses_moq": False,
    "methods": [
        {"name": "Get_ExistingId_Returns200", "kind": "Fact", "returns": "Task"},
        {"name": "Get_MissingId_Returns404", "kind": "Fact", "returns": "Task"},
        {"name": "Get_VariousIds_ReturnsExpected", "kind": "Theory", "returns": "Task"},
    ],
}
BAD = {
    "test_class": "OrdersTests",
    "scope": "integration",
    "fixture": "none",
    "all_async_return_task": False,
    "uses_fluent_assertions": False,
    "uses_moq": True,
    "methods": [{"name": "test1", "kind": "Fact", "returns": "void"}],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
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
