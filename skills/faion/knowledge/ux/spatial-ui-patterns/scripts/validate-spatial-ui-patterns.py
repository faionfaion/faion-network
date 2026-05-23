#!/usr/bin/env python3
"""validate-spatial-ui-patterns.py

Validate the artefact for the spatial-ui-patterns methodology against the schema in
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
PANEL_TYPES = {'head-locked', 'world-locked', 'body-locked', 'hand-attached'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'spatial-ui-patterns':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'spec':
            errs.append("__faion_header__.produces mismatch")
    if 'platforms' not in obj:
        errs.append(f"missing required field: " + 'platforms')
    if 'panels' not in obj:
        errs.append(f"missing required field: " + 'panels')


    plats = obj.get("platforms") or []
    if not isinstance(plats, list) or not plats:
        errs.append("platforms must be non-empty list")
    panels = obj.get("panels") or []
    if not isinstance(panels, list) or not panels:
        errs.append("panels must be non-empty list")
    primary_fov_sum = 0
    for i, p in enumerate(panels):
        t = p.get("type")
        if t not in PANEL_TYPES:
            errs.append("panels[" + str(i) + "].type invalid")
        d = p.get("distance_m")
        if not isinstance(d, (int, float)) or d < 0.3:
            errs.append("panels[" + str(i) + "].distance_m invalid")
        mtp = p.get("min_target_pt")
        if not isinstance(mtp, (int, float)) or mtp < 60:
            errs.append("panels[" + str(i) + "].min_target_pt must be >=60")
        if p.get("primary") is True and t == "head-locked":
            if "visionos" in plats and not p.get("head_locked_justification"):
                errs.append("panels[" + str(i) + "] primary head-locked on visionOS requires head_locked_justification")
        if p.get("primary") is True and isinstance(d, (int, float)) and d < 1.0:
            errs.append("panels[" + str(i) + "] primary panel distance must be >=1.0 m")
        if p.get("primary") is True:
            fov = p.get("fov_occupancy_pct") or 0
            primary_fov_sum += fov
    if primary_fov_sum > 40:
        errs.append("sum of primary panel fov_occupancy_pct must be <=40")

    return errs


OK = {'__faion_header__': {'methodology': 'spatial-ui-patterns', 'version': '1.1.0', 'produces': 'spec'}, 'platforms': ['visionos', 'quest'], 'panels': [{'id': 'main-window', 'type': 'body-locked', 'distance_m': 1.8, 'min_target_pt': 60, 'primary': True, 'fov_occupancy_pct': 28}, {'id': 'battery-warning', 'type': 'head-locked', 'distance_m': 1.5, 'min_target_pt': 60, 'primary': False, 'fov_occupancy_pct': 3, 'head_locked_justification': 'safety telemetry; appears only when battery <10%'}]}
BAD = {'platforms': ['visionos'], 'panels': [{'id': 'hud', 'type': 'head-locked', 'distance_m': 0.5, 'min_target_pt': 24, 'primary': True}]}


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
