#!/usr/bin/env python3
"""validate-java-spring.py

Validate the service-scaffold manifest for the java-spring methodology against
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
import re
import sys
from pathlib import Path

REQUIRED = [
    "spring_boot_version",
    "endpoints",
    "uses_mapstruct",
    "uses_bcrypt_in_service",
    "jakarta_imports_only",
]
SB_RE = re.compile(r"^3\.")
METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not SB_RE.match(str(obj.get("spring_boot_version", ""))):
        errs.append("spring_boot_version must start with 3.")
    endpoints = obj.get("endpoints") or []
    if not isinstance(endpoints, list) or len(endpoints) < 1:
        errs.append("endpoints must be non-empty list")
    for i, e in enumerate(endpoints):
        if e.get("method") not in METHODS:
            errs.append(f"endpoints[{i}].method must be one of {sorted(METHODS)}")
        if e.get("returns_dto") is not True:
            errs.append(f"endpoints[{i}].returns_dto must be true")
        if e.get("method") == "GET" and e.get("list_pageable") is False:
            errs.append(f"endpoints[{i}] GET list must support Pageable")
        if e.get("method") in WRITE_METHODS and e.get("transactional_on_write") is False:
            errs.append(f"endpoints[{i}] write method missing @Transactional")
    if obj.get("uses_mapstruct") is not True:
        errs.append("uses_mapstruct must be true")
    if obj.get("uses_bcrypt_in_service") is not True:
        errs.append("uses_bcrypt_in_service must be true")
    if obj.get("jakarta_imports_only") is not True:
        errs.append("jakarta_imports_only must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "spring_boot_version": "3.2.1",
    "endpoints": [
        {"path": "/api/v1/users", "method": "GET", "returns_dto": True, "list_pageable": True, "transactional_on_write": False},
        {"path": "/api/v1/users", "method": "POST", "returns_dto": True, "list_pageable": None, "transactional_on_write": True},
    ],
    "uses_mapstruct": True,
    "uses_bcrypt_in_service": True,
    "jakarta_imports_only": True,
    "forbidden_patterns_found": [],
}
BAD = {
    "spring_boot_version": "2.7.0",
    "endpoints": [{"path": "/api/v1/users", "method": "GET", "returns_dto": False, "list_pageable": False, "transactional_on_write": False}],
    "uses_mapstruct": False,
    "uses_bcrypt_in_service": False,
    "jakarta_imports_only": False,
    "forbidden_patterns_found": ["javax.persistence"],
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
