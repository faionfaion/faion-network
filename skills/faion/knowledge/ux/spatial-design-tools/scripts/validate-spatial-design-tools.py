#!/usr/bin/env python3
"""validate-spatial-design-tools.py

Validate the artefact for the spatial-design-tools methodology against the schema in
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
PHASES = {'concept', 'production', 'prototype'}
PLATFORMS = {'webxr', 'visionos', 'quest', 'android-xr', 'psvr2', 'hololens'}
FORMATS = {'usdz', 'usd', 'glb', 'gltf'}
ENGINES = {'realitycomposer-pro', 'unreal', 'godot', 'unity'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'spatial-design-tools':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'config':
            errs.append("__faion_header__.produces mismatch")
    if 'phase' not in obj:
        errs.append(f"missing required field: " + 'phase')
    if 'platforms' not in obj:
        errs.append(f"missing required field: " + 'platforms')
    if 'tool_stack' not in obj:
        errs.append(f"missing required field: " + 'tool_stack')
    if 'asset_format' not in obj:
        errs.append(f"missing required field: " + 'asset_format')
    if 'budgets' not in obj:
        errs.append(f"missing required field: " + 'budgets')


    if obj.get("phase") not in PHASES:
        errs.append("phase invalid")
    plats = obj.get("platforms") or []
    if not isinstance(plats, list) or not plats:
        errs.append("platforms must be non-empty list")
    else:
        for p in plats:
            if p not in PLATFORMS:
                errs.append("platform invalid: " + str(p))
    ts = obj.get("tool_stack") or {}
    for k in ("concept", "prototype", "production"):
        v = ts.get(k) or []
        if not isinstance(v, list) or not v:
            errs.append("tool_stack." + k + " must be non-empty list")
    proto = ts.get("prototype") or []
    if len(proto) > 1:
        errs.append("tool_stack.prototype must contain exactly one engine")
    prod = ts.get("production") or []
    if len(prod) > 1:
        errs.append("tool_stack.production must contain exactly one engine")
    fmt = obj.get("asset_format") or {}
    if fmt.get("primary") not in FORMATS:
        errs.append("asset_format.primary invalid")
    b = obj.get("budgets") or {}
    for k in ("polygon_max", "file_size_mb_max", "draw_calls_max"):
        if k not in b:
            errs.append("budgets." + k + " missing")

    return errs


OK = {'__faion_header__': {'methodology': 'spatial-design-tools', 'version': '1.1.0', 'produces': 'config'}, 'phase': 'prototype', 'platforms': ['visionos', 'quest'], 'tool_stack': {'concept': ['figma', 'shapesxr'], 'prototype': ['unity'], 'production': ['unity']}, 'asset_format': {'primary': 'gltf', 'secondary': ['usdz']}, 'budgets': {'polygon_max': 100000, 'file_size_mb_max': 30, 'draw_calls_max': 100}, 'engine_rationale': 'Team has 4 years Unity; Quest XR SDK + PolySpatial cover both targets.'}
BAD = {'phase': 'prototype', 'platforms': ['quest'], 'tool_stack': {'prototype': ['unity', 'unreal']}, 'budgets': {}}


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
