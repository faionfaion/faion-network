#!/usr/bin/env python3
"""validate-java-spring-boot.py

Validate the layered-service manifest for the java-spring-boot methodology
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
    "spring_boot_version",
    "stack",
    "uses_records_for_dtos",
    "uses_mapstruct",
    "uses_problemdetail_advice",
    "injection_style",
]
SB_RE = re.compile(r"^3\.")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not SB_RE.match(str(obj.get("spring_boot_version", ""))):
        errs.append("spring_boot_version must start with 3.")
    if obj.get("stack") != "webmvc":
        errs.append("stack must be 'webmvc'")
    if obj.get("uses_records_for_dtos") is not True:
        errs.append("uses_records_for_dtos must be true")
    if obj.get("uses_mapstruct") is not True:
        errs.append("uses_mapstruct must be true")
    if obj.get("uses_problemdetail_advice") is not True:
        errs.append("uses_problemdetail_advice must be true")
    if obj.get("injection_style") != "constructor":
        errs.append("injection_style must be 'constructor'")
    if obj.get("transactional_layer") and obj.get("transactional_layer") != "service":
        errs.append("transactional_layer must be 'service'")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "spring_boot_version": "3.2.1",
    "stack": "webmvc",
    "uses_records_for_dtos": True,
    "uses_mapstruct": True,
    "uses_problemdetail_advice": True,
    "injection_style": "constructor",
    "transactional_layer": "service",
    "forbidden_patterns_found": [],
}
BAD = {
    "spring_boot_version": "2.7.0",
    "stack": "webflux",
    "uses_records_for_dtos": False,
    "uses_mapstruct": False,
    "uses_problemdetail_advice": False,
    "injection_style": "field",
    "transactional_layer": "controller",
    "forbidden_patterns_found": ["@Autowired field"],
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
