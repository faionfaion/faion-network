#!/usr/bin/env python3
"""validate-csharp-dotnet-patterns.py

Validate the layered-solution manifest for the csharp-dotnet-patterns methodology
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
import sys
from pathlib import Path

REQUIRED = ["solution_name", "projects", "use_cases", "arch_tests_pass", "outbox_configured"]
PROJECTS = ["Domain", "Application", "Infrastructure", "Api"]
ALLOWED_REFS = {
    "Domain": set(),
    "Application": {"Domain"},
    "Infrastructure": {"Domain", "Application"},
    "Api": {"Application", "Infrastructure"},
}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    name = obj.get("solution_name", "")
    if not (isinstance(name, str) and name[:1].isupper() and name.replace("_", "").isalnum()):
        errs.append("solution_name must be PascalCase")
    projects = obj.get("projects") or {}
    for p in PROJECTS:
        if p not in projects:
            errs.append(f"projects.{p} missing")
            continue
        refs = set(projects[p].get("references", []))
        leaks = refs - ALLOWED_REFS[p]
        if leaks:
            errs.append(f"projects.{p}.references leaks to: {sorted(leaks)}")
    uc = obj.get("use_cases") or []
    if not isinstance(uc, list) or len(uc) < 1:
        errs.append("use_cases must be non-empty list")
    if obj.get("arch_tests_pass") is not True:
        errs.append("arch_tests_pass must be true")
    if obj.get("outbox_configured") is not True:
        errs.append("outbox_configured must be true")
    return errs


OK = {
    "solution_name": "Billing",
    "projects": {
        "Domain": {"references": []},
        "Application": {"references": ["Domain"]},
        "Infrastructure": {"references": ["Domain", "Application"]},
        "Api": {"references": ["Application", "Infrastructure"]},
    },
    "use_cases": [{"feature": "Invoices", "name": "CreateInvoice"}],
    "arch_tests_pass": True,
    "outbox_configured": True,
}
BAD = {
    "solution_name": "billing",
    "projects": {
        "Domain": {"references": ["Infrastructure"]},
        "Application": {"references": ["Domain", "Infrastructure"]},
        "Infrastructure": {"references": ["Domain"]},
        "Api": {"references": ["Application"]},
    },
    "use_cases": [],
    "arch_tests_pass": False,
    "outbox_configured": False,
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
