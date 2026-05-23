#!/usr/bin/env python3
"""validate-decomposition-rails.py

Validate the structural-lint manifest for the decomposition-rails methodology
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
    "ruby_version",
    "rails_version",
    "services",
    "query_objects",
    "form_objects",
    "namespace_whitelist_passed",
    "file_size_budgets",
]
RUBY_RE = re.compile(r"^3\.")
RAILS_RE = re.compile(r"^(7|8)\.")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not RUBY_RE.match(str(obj.get("ruby_version", ""))):
        errs.append("ruby_version must start with 3.")
    if not RAILS_RE.match(str(obj.get("rails_version", ""))):
        errs.append("rails_version must start with 7 or 8")
    services = obj.get("services") or []
    if not isinstance(services, list) or len(services) < 1:
        errs.append("services must be non-empty list")
    for i, s in enumerate(services):
        if not str(s.get("class", "")).endswith("Service"):
            errs.append(f"services[{i}].class must end with 'Service'")
        if s.get("returns") in ("void", "nil"):
            errs.append(f"services[{i}].returns must not be void/nil")
    for i, q in enumerate(obj.get("query_objects") or []):
        if not str(q.get("class", "")).endswith("Query"):
            errs.append(f"query_objects[{i}].class must end with 'Query'")
        if q.get("reuses_scopes") is not True:
            errs.append(f"query_objects[{i}].reuses_scopes must be true")
    for i, f in enumerate(obj.get("form_objects") or []):
        if not str(f.get("class", "")).endswith("Form"):
            errs.append(f"form_objects[{i}].class must end with 'Form'")
        if f.get("base") != "ActiveModel::Model":
            errs.append(f"form_objects[{i}].base must be 'ActiveModel::Model'")
    if obj.get("namespace_whitelist_passed") is not True:
        errs.append("namespace_whitelist_passed must be true")
    b = obj.get("file_size_budgets") or {}
    if b.get("service_max", 999) > 100:
        errs.append("file_size_budgets.service_max must be <= 100")
    if b.get("controller_max", 999) > 150:
        errs.append("file_size_budgets.controller_max must be <= 150")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "ruby_version": "3.3",
    "rails_version": "7.1",
    "services": [{"class": "Users::CreateService", "returns": "User"}],
    "query_objects": [{"class": "Users::ActiveUsersQuery", "reuses_scopes": True}],
    "form_objects": [{"class": "Users::SignupForm", "base": "ActiveModel::Model"}],
    "namespace_whitelist_passed": True,
    "file_size_budgets": {"service_max": 88, "controller_max": 132},
    "forbidden_patterns_found": [],
}
BAD = {
    "ruby_version": "2.7",
    "rails_version": "6.0",
    "services": [{"class": "UserManager", "returns": "void"}],
    "query_objects": [{"class": "ActiveUsers", "reuses_scopes": False}],
    "form_objects": [{"class": "SignupForm", "base": "ActiveRecord::Base"}],
    "namespace_whitelist_passed": False,
    "file_size_budgets": {"service_max": 320, "controller_max": 480},
    "forbidden_patterns_found": ["app/managers/ namespace"],
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
