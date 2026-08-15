#!/usr/bin/env python3
"""validate-ruby-rspec-testing.py

Validate the code artefact for the ruby-rspec-testing methodology against the schema in
02-output-contract.xml.

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

REQUIRED = ['spec_file', 'uses_describe_context_it', 'uses_build_stubbed_when_possible', 'isolated_when_unit', 'no_unused_let_bang']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    return errs


OK = {'spec_file': 'spec/services/orders/place_order_service_spec.rb', 'uses_describe_context_it': True, 'uses_build_stubbed_when_possible': True, 'isolated_when_unit': True, 'uses_shared_examples_for_invariants': True, 'no_unused_let_bang': True, 'lines': 120}
BAD = {'uses_describe_context_it': False, 'uses_build_stubbed_when_possible': False, 'isolated_when_unit': False, 'uses_shared_examples_for_invariants': False, 'no_unused_let_bang': False, 'lines': 600}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
        sys.stderr.write(f"not a file: {p}\n"); return 2
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
