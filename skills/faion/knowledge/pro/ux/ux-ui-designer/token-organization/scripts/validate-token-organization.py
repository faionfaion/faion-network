#!/usr/bin/env python3
"""validate-token-organization.py

Validate the artefact for the token-organization methodology against the schema in
content/02-output-contract.xml.

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

VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
TIERS = {'primitives', 'semantic', 'component'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'token-organization':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'config':
            errs.append("__faion_header__.produces mismatch")
    if 'tiers' not in obj:
        errs.append(f"missing required field: " + 'tiers')
    if 'naming_convention' not in obj:
        errs.append(f"missing required field: " + 'naming_convention')
    if 'tokens' not in obj:
        errs.append(f"missing required field: " + 'tokens')
    if 'lint' not in obj:
        errs.append(f"missing required field: " + 'lint')


    t = obj.get("tiers") or []
    if t != ["primitives", "semantic", "component"]:
        errs.append("tiers must be exactly ['primitives','semantic','component']")
    if obj.get("naming_convention") != "{category}.{property}.{variant}.{state}":
        errs.append("naming_convention mismatch")
    tk = obj.get("tokens") or {}
    for k in ("primitives", "semantic", "component"):
        if k not in tk:
            errs.append("tokens." + k + " missing")
    lint = obj.get("lint") or {}
    for k in ("reject_primitive_in_component", "reject_raw_values_above_primitives", "require_state_suffix"):
        if lint.get(k) is not True:
            errs.append("lint." + k + " must be true")

    return errs


OK = {'__faion_header__': {'methodology': 'token-organization', 'version': '1.1.0', 'produces': 'config'}, 'tiers': ['primitives', 'semantic', 'component'], 'naming_convention': '{category}.{property}.{variant}.{state}', 'tokens': {'primitives': {'color.blue.600': '#0066cc'}, 'semantic': {'color.action.primary.default': '{color.blue.600}', 'color.action.primary.hover': '{color.blue.700}'}, 'component': {'button.primary.background.default': '{color.action.primary.default}'}}, 'lint': {'reject_primitive_in_component': True, 'reject_raw_values_above_primitives': True, 'require_state_suffix': True}}
BAD = {'tiers': ['primitives', 'semantic'], 'naming_convention': 'color-action-primary', 'tokens': {'semantic': {'primary': '#0066cc'}}}


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
