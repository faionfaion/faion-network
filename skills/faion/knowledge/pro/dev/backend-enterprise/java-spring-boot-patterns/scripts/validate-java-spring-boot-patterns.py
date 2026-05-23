#!/usr/bin/env python3
"""validate-java-spring-boot-patterns.py

Validate the enterprise-service manifest for the java-spring-boot-patterns
methodology against the JSON Schema declared in 02-output-contract.xml.

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
    "base_entity",
    "uses_record_dtos",
    "uses_mapstruct",
    "service_readonly_default",
    "search_strategy",
    "uses_problemdetail_advice",
    "actuator_enabled",
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
    be = obj.get("base_entity") or {}
    if be.get("pk_type") != "UUID":
        errs.append("base_entity.pk_type must be 'UUID'")
    if be.get("has_audit") is not True:
        errs.append("base_entity.has_audit must be true")
    if be.get("has_version") is not True:
        errs.append("base_entity.has_version must be true")
    if obj.get("uses_record_dtos") is not True:
        errs.append("uses_record_dtos must be true")
    if obj.get("uses_mapstruct") is not True:
        errs.append("uses_mapstruct must be true")
    if obj.get("service_readonly_default") is not True:
        errs.append("service_readonly_default must be true")
    if obj.get("search_strategy") != "JpaSpecificationExecutor":
        errs.append("search_strategy must be 'JpaSpecificationExecutor'")
    if obj.get("uses_problemdetail_advice") is not True:
        errs.append("uses_problemdetail_advice must be true")
    if obj.get("actuator_enabled") is not True:
        errs.append("actuator_enabled must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "spring_boot_version": "3.2.1",
    "base_entity": {"pk_type": "UUID", "has_audit": True, "has_version": True},
    "uses_record_dtos": True,
    "uses_mapstruct": True,
    "service_readonly_default": True,
    "search_strategy": "JpaSpecificationExecutor",
    "uses_problemdetail_advice": True,
    "actuator_enabled": True,
    "forbidden_patterns_found": [],
}
BAD = {
    "spring_boot_version": "2.7.0",
    "base_entity": {"pk_type": "Long", "has_audit": False, "has_version": False},
    "uses_record_dtos": False,
    "uses_mapstruct": False,
    "service_readonly_default": False,
    "search_strategy": "JpqlConcat",
    "uses_problemdetail_advice": False,
    "actuator_enabled": False,
    "forbidden_patterns_found": ["@Data on entity"],
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
