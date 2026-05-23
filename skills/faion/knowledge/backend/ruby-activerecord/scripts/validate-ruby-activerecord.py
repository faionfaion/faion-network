#!/usr/bin/env python3
"""validate-ruby-activerecord.py

Validate the AR-discipline manifest for the ruby-activerecord methodology against
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

REQUIRED = ["rails_version", "ruby_version", "query_objects", "uses_default_scope", "n_plus_one_gate_enabled"]
RAILS_RE = re.compile(r"^(7|8)\.")
RUBY_RE = re.compile(r"^3\.")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not RAILS_RE.match(str(obj.get("rails_version", ""))):
        errs.append("rails_version must be 7.x or 8.x")
    if not RUBY_RE.match(str(obj.get("ruby_version", ""))):
        errs.append("ruby_version must start with 3.")
    for i, q in enumerate(obj.get("query_objects") or []):
        if not str(q.get("class", "")).endswith("Query"):
            errs.append(f"query_objects[{i}].class must end with 'Query'")
        if q.get("exposes_results_as_relation") is not True:
            errs.append(f"query_objects[{i}].exposes_results_as_relation must be true")
        if not isinstance(q.get("method_count"), int) or q.get("method_count", 0) > 10:
            errs.append(f"query_objects[{i}].method_count must be <= 10")
    if obj.get("uses_default_scope") is not False:
        errs.append("uses_default_scope must be false")
    if obj.get("n_plus_one_gate_enabled") is not True:
        errs.append("n_plus_one_gate_enabled must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "rails_version": "7.1",
    "ruby_version": "3.3",
    "query_objects": [{"class": "Users::ActiveUsersQuery", "exposes_results_as_relation": True, "method_count": 6}],
    "uses_default_scope": False,
    "n_plus_one_gate_enabled": True,
    "forbidden_patterns_found": [],
}
BAD = {
    "rails_version": "6.0",
    "ruby_version": "2.7",
    "query_objects": [{"class": "UserQueryGodObject", "exposes_results_as_relation": False, "method_count": 32}],
    "uses_default_scope": True,
    "n_plus_one_gate_enabled": False,
    "forbidden_patterns_found": ["default_scope"],
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
