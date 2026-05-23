#!/usr/bin/env python3
"""validate-vui-iot-integration.py

Validate the artefact for the vui-iot-integration methodology against the schema in
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


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'vui-iot-integration':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'config':
            errs.append("__faion_header__.produces mismatch")
    if 'groups' not in obj:
        errs.append(f"missing required field: " + 'groups')
    if 'scenes' not in obj:
        errs.append(f"missing required field: " + 'scenes')
    if 'routines' not in obj:
        errs.append(f"missing required field: " + 'routines')
    if 'partial_failure_feedback' not in obj:
        errs.append(f"missing required field: " + 'partial_failure_feedback')
    if 'undo_supported' not in obj:
        errs.append(f"missing required field: " + 'undo_supported')
    if 'noise_conditions' not in obj:
        errs.append(f"missing required field: " + 'noise_conditions')


    groups = obj.get("groups") or []
    if not isinstance(groups, list) or not groups:
        errs.append("groups must be non-empty list")
    for i, g in enumerate(groups):
        if not g.get("device_ids"):
            errs.append("groups[" + str(i) + "].device_ids missing")
    scenes = obj.get("scenes") or []
    for i, s in enumerate(scenes):
        name = s.get("name") or ""
        if len(name) < 3:
            errs.append("scenes[" + str(i) + "].name too short")
    if obj.get("partial_failure_feedback") is not True:
        errs.append("partial_failure_feedback must be true")
    if obj.get("undo_supported") is not True:
        errs.append("undo_supported must be true")
    nc = obj.get("noise_conditions") or []
    if not isinstance(nc, list) or len(nc) < 3:
        errs.append("noise_conditions must have >=3")

    return errs


OK = {'__faion_header__': {'methodology': 'vui-iot-integration', 'version': '1.1.0', 'produces': 'config'}, 'groups': [{'id': 'bedroom', 'name': 'bedroom', 'device_ids': ['hue-001', 'nest-thermo-002']}], 'scenes': [{'name': 'good night', 'actions': [{'device_id': 'hue-001', 'action': 'off'}, {'device_id': 'nest-thermo-002', 'action': 'set', 'value': 18}]}], 'routines': [{'name': 'movie night'}], 'partial_failure_feedback': True, 'undo_supported': True, 'noise_conditions': ['quiet', 'kitchen', 'tv']}
BAD = {'groups': [], 'scenes': [{'name': 'S1'}], 'routines': [], 'partial_failure_feedback': False, 'undo_supported': False, 'noise_conditions': ['quiet']}


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
