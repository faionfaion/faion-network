#!/usr/bin/env python3
"""validate-spatial-interaction-patterns.py

Validate the artefact for the spatial-interaction-patterns methodology against the schema in
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
PLATFORMS = {'android-xr', 'hololens', 'webxr', 'visionos', 'psvr2', 'quest'}
MODALITIES = {'voice', 'gesture', 'hand-raycast', 'hand-direct', 'gaze+dwell', 'controller'}
STATES = {'hover', 'error', 'idle', 'active', 'cancel'}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != 'spatial-interaction-patterns':
            errs.append("__faion_header__.methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != 'spec':
            errs.append("__faion_header__.produces mismatch")
    if 'platforms' not in obj:
        errs.append(f"missing required field: " + 'platforms')
    if 'interactions' not in obj:
        errs.append(f"missing required field: " + 'interactions')


    plats = obj.get("platforms") or []
    if not isinstance(plats, list) or not plats:
        errs.append("platforms must be non-empty list")
    else:
        for p in plats:
            if p not in PLATFORMS:
                errs.append("platform invalid: " + str(p))
    inters = obj.get("interactions") or []
    if not isinstance(inters, list) or not inters:
        errs.append("interactions must be non-empty list")
    else:
        for i, it in enumerate(inters):
            for k in ("name", "primary_modality", "fallback_modality", "state_machine"):
                if k not in it:
                    errs.append("interactions[" + str(i) + "] missing " + k)
            pm = it.get("primary_modality")
            fm = it.get("fallback_modality")
            if pm not in MODALITIES:
                errs.append("interactions[" + str(i) + "].primary_modality invalid")
            if fm not in MODALITIES:
                errs.append("interactions[" + str(i) + "].fallback_modality invalid")
            if pm and pm == fm:
                errs.append("interactions[" + str(i) + "] primary == fallback")
            sm = it.get("state_machine") or []
            for must in ("idle", "hover", "active", "cancel", "error"):
                if must not in sm:
                    errs.append("interactions[" + str(i) + "].state_machine missing " + must)

    return errs


OK = {'__faion_header__': {'methodology': 'spatial-interaction-patterns', 'version': '1.1.0', 'produces': 'spec'}, 'platforms': ['visionos', 'quest'], 'interactions': [{'name': 'select-window', 'primary_modality': 'gaze+dwell', 'fallback_modality': 'voice', 'state_machine': ['idle', 'hover', 'active', 'cancel', 'error'], 'per_platform_notes': {'quest': 'hand-raycast tap also accepted'}}]}
BAD = {'platforms': ['quest'], 'interactions': [{'name': 'grab', 'primary_modality': 'hand-direct', 'state_machine': ['idle', 'active']}]}


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
