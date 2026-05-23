#!/usr/bin/env python3
"""validate-w3c-design-tokens-standard.py

Validate the artefact for the w3c-design-tokens-standard methodology against the schema in
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

REQUIRED = ['primitive', 'semantic']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    prim = obj.get("primitive") or {}
    sem = obj.get("semantic") or {}
    def walk(node, errors, parent_key=""):
        if isinstance(node, dict):
            if "$value" in node and "$type" not in node:
                errors.append(f"token missing $type at {parent_key}")
            for k, v in node.items():
                walk(v, errors, parent_key + "/" + k)
    walk(prim, errs, "primitive")
    walk(sem, errs, "semantic")

    return errs


OK = {   'primitive': {   'color': {   'blue-500': {   '$type': 'color',
                                                  '$value': '#2563EB',
                                                  '$description': 'Brand primary'},
                                  'gray-900': {'$type': 'color', '$value': '#111827'},
                                  'white': {'$type': 'color', '$value': '#FFFFFF'}}},
    'semantic': {   'color': {   'text-primary': {'$type': 'color', '$value': '{color.gray-900}'},
                                 'background-canvas': {'$type': 'color', '$value': '{color.white}'},
                                 'brand-primary': {   '$type': 'color',
                                                      '$value': '{color.blue-500}'}}},
    'resolved_alias_count': 3}
BAD = {'primitive': {'color': {'blue-500': {'$value': '#2563EB'}}}}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"ok rejected: {errs_ok}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
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
