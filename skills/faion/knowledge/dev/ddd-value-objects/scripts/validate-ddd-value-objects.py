#!/usr/bin/env python3
"""validate-ddd-value-objects.py

Validate a value-object spec against the schema in 02-output-contract.xml.

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

REQUIRED = ["class_name", "immutable", "constructor_validation", "value_equality", "has_identity_field"]
NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")
OP_RE = re.compile(r"^[a-z][a-z0-9_]+$")
LANGS = {"python", "csharp", "java", "kotlin", "typescript"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "class_name" in obj and not NAME_RE.match(str(obj["class_name"])):
        errs.append("class_name must be PascalCase")
    if obj.get("immutable") is not True:
        errs.append("immutable must be true (immutability)")
    if obj.get("constructor_validation") is not True:
        errs.append("constructor_validation must be true")
    if obj.get("value_equality") is not True:
        errs.append("value_equality must be true")
    if obj.get("has_identity_field") is True:
        errs.append("has_identity_field must be false (no-identity)")
    if obj.get("language") and obj["language"] not in LANGS:
        errs.append(f"language must be one of {sorted(LANGS)}")
    for op in obj.get("ops") or []:
        if not OP_RE.match(str(op.get("name", ""))):
            errs.append(f"op name '{op.get('name')}' must be snake_case")
        if op.get("returns_new_instance") is not True:
            errs.append(f"op '{op.get('name')}' must return new instance (ops-return-new)")
    return errs


OK = {
    "class_name": "Money",
    "immutable": True,
    "constructor_validation": True,
    "value_equality": True,
    "has_identity_field": False,
    "language": "python",
    "ops": [
        {"name": "add", "returns_new_instance": True},
        {"name": "subtract", "returns_new_instance": True},
    ],
}
BAD = {
    "class_name": "money",
    "immutable": False,
    "constructor_validation": False,
    "value_equality": False,
    "has_identity_field": True,
    "language": "python",
    "ops": [{"name": "Add", "returns_new_instance": False}],
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
