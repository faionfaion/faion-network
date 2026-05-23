#!/usr/bin/env python3
"""validate-spatial-ux-fundamentals.py

Validate the artefact for the spatial-ux-fundamentals methodology against the schema in
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
PLATFORMS = {'android-xr', 'visionos', 'webxr', 'quest', 'hololens', 'psvr2'}
ZONES = {'mid', 'near', 'far'}
ANCHORS = {'head-locked', 'head-locked-with-decay', 'hand-attached', 'world-locked'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'spatial-ux-fundamentals':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'spec':
            errs.append("__faion_header__.produces mismatch")
    if 'platform' not in obj:
        errs.append(f"missing required field: " + 'platform')
    if 'elements' not in obj:
        errs.append(f"missing required field: " + 'elements')
    if 'recenter_affordance' not in obj:
        errs.append(f"missing required field: " + 'recenter_affordance')


    if obj.get("platform") not in PLATFORMS:
        errs.append("platform invalid")
    elems = obj.get("elements") or []
    if not isinstance(elems, list) or not elems:
        errs.append("elements must be non-empty list")
    for i, e in enumerate(elems):
        z = e.get("zone")
        if z not in ZONES:
            errs.append("elements[" + str(i) + "].zone invalid")
        d = e.get("distance_m")
        if not isinstance(d, (int, float)) or d < 0.3:
            errs.append("elements[" + str(i) + "].distance_m invalid")
        if e.get("interactive") is True and z == "far":
            errs.append("elements[" + str(i) + "] interactive in far field forbidden")
        a = e.get("anchor")
        if a not in ANCHORS:
            errs.append("elements[" + str(i) + "].anchor invalid")
        if e.get("interactive") is True and a == "world-locked":
            errs.append("elements[" + str(i) + "] interactive must not be world-locked")
        if e.get("in_chin_region") is True:
            errs.append("elements[" + str(i) + "] in chin region forbidden")
    ra = obj.get("recenter_affordance") or {}
    if ra.get("button") is not True or ra.get("voice_command") is not True:
        errs.append("recenter_affordance must include button + voice_command")

    return errs


OK = {'__faion_header__': {'methodology': 'spatial-ux-fundamentals', 'version': '1.1.0', 'produces': 'spec'}, 'platform': 'visionos', 'elements': [{'id': 'main-window', 'zone': 'mid', 'distance_m': 1.8, 'interactive': True, 'anchor': 'head-locked-with-decay', 'in_chin_region': False}, {'id': 'ambient-clock', 'zone': 'far', 'distance_m': 4.0, 'interactive': False, 'anchor': 'world-locked', 'in_chin_region': False}], 'recenter_affordance': {'button': True, 'voice_command': True}}
BAD = {'platform': 'quest', 'elements': [{'id': 'cta', 'zone': 'far', 'distance_m': 4.0, 'interactive': True, 'anchor': 'world-locked'}], 'recenter_affordance': {'button': False, 'voice_command': False}}


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
