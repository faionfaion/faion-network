#!/usr/bin/env python3
"""validate-vr-design-patterns.py

Validate the artefact for the vr-design-patterns methodology against the schema in
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
        if hdr.get("methodology") != 'vr-design-patterns':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'spec':
            errs.append("__faion_header__.produces mismatch")
    if 'scenes' not in obj:
        errs.append(f"missing required field: " + 'scenes')
    if 'locomotion' not in obj:
        errs.append(f"missing required field: " + 'locomotion')
    if 'ui_anchoring' not in obj:
        errs.append(f"missing required field: " + 'ui_anchoring')
    if 'accessibility' not in obj:
        errs.append(f"missing required field: " + 'accessibility')


    scenes = obj.get("scenes") or []
    if not isinstance(scenes, list) or not scenes:
        errs.append("scenes must be non-empty list")
    for i, s in enumerate(scenes):
        if s.get("has_ground") is not True:
            errs.append("scenes[" + str(i) + "].has_ground must be true")
        if s.get("has_horizon") is not True:
            errs.append("scenes[" + str(i) + "].has_horizon must be true")
    loc = obj.get("locomotion") or {}
    if loc.get("default") != "teleport":
        errs.append("locomotion.default must be 'teleport'")
    opts = loc.get("options") or []
    if not isinstance(opts, list) or len(opts) < 2:
        errs.append("locomotion.options must have >=2")
    turn = loc.get("turning") or {}
    if turn.get("default") != "snap":
        errs.append("locomotion.turning.default must be 'snap'")
    turn_opts = turn.get("options") or []
    if not isinstance(turn_opts, list) or len(turn_opts) < 2:
        errs.append("locomotion.turning.options must have >=2")
    uia = obj.get("ui_anchoring") or {}
    if uia.get("primary") not in ("world-anchored", "body-anchored"):
        errs.append("ui_anchoring.primary must be world-anchored or body-anchored")
    a = obj.get("accessibility") or {}
    for k in ("seated_toggle", "one_handed_path", "subtitles", "audio_descriptions"):
        if a.get(k) is not True:
            errs.append("accessibility." + k + " must be true")

    return errs


OK = {'__faion_header__': {'methodology': 'vr-design-patterns', 'version': '1.1.0', 'produces': 'spec'}, 'scenes': [{'id': 'lobby', 'has_ground': True, 'has_horizon': True}, {'id': 'arena', 'has_ground': True, 'has_horizon': True}], 'locomotion': {'default': 'teleport', 'options': ['teleport', 'smooth'], 'turning': {'default': 'snap', 'options': ['snap', 'smooth']}}, 'ui_anchoring': {'primary': 'world-anchored', 'head_locked_for_safety_only': True}, 'accessibility': {'seated_toggle': True, 'one_handed_path': True, 'subtitles': True, 'audio_descriptions': True}}
BAD = {'scenes': [{'id': 'space', 'has_ground': False, 'has_horizon': False}], 'locomotion': {'default': 'smooth', 'options': ['smooth'], 'turning': {'default': 'smooth', 'options': ['smooth']}}, 'ui_anchoring': {'primary': 'head-locked'}, 'accessibility': {'seated_toggle': False}}


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
