#!/usr/bin/env python3
"""validate-spatial-accessibility.py

Validate a spatial-accessibility audit JSON against the schema in
content/02-output-contract.xml.

Inputs:
    --file PATH       path to audit JSON
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
ALLOWED_PLATFORMS = {"visionos", "quest", "psvr2", "hololens", "webxr"}
ALLOWED_MODALITIES = {"gaze+dwell", "voice", "single-hand", "two-hand", "controller", "switch"}
ALLOWED_LOCO = {"vignette", "teleport", "smooth"}
ALLOWED_TURN = {"snap", "smooth"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__")
    else:
        if hdr.get("methodology") != "spatial-accessibility":
            errs.append("header methodology mismatch")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("header version not semver")
        if hdr.get("produces") != "report":
            errs.append("header produces mismatch")

    if obj.get("platform") not in ALLOWED_PLATFORMS:
        errs.append("platform invalid")

    inters = obj.get("interactions")
    if not isinstance(inters, list) or not inters:
        errs.append("interactions must be non-empty list")
    else:
        for i, it in enumerate(inters):
            for k in ("name", "primary_modality", "alternative_modalities", "seated_compatible", "non_spatial_fallback"):
                if k not in it:
                    errs.append(f"interactions[{i}] missing {k}")
            if it.get("primary_modality") not in ALLOWED_MODALITIES:
                errs.append(f"interactions[{i}].primary_modality invalid")
            alts = it.get("alternative_modalities") or []
            if not isinstance(alts, list) or len(alts) < 1:
                errs.append(f"interactions[{i}].alternative_modalities must have >=1")
            else:
                for a in alts:
                    if a not in ALLOWED_MODALITIES:
                        errs.append(f"interactions[{i}].alternative_modalities has invalid {a}")
            if not isinstance(it.get("seated_compatible"), bool):
                errs.append(f"interactions[{i}].seated_compatible must be bool")
            if not it.get("non_spatial_fallback"):
                errs.append(f"interactions[{i}].non_spatial_fallback empty")

    co = obj.get("comfort_options")
    if not isinstance(co, dict):
        errs.append("comfort_options missing")
    else:
        loco = co.get("locomotion") or []
        if not isinstance(loco, list) or len(loco) < 2:
            errs.append("comfort_options.locomotion must have >=2 options")
        if "smooth" in loco and "vignette" not in loco and "teleport" not in loco:
            errs.append("locomotion smooth-only is forbidden")
        if not any(x in loco for x in ("vignette", "teleport")):
            errs.append("locomotion must include vignette or teleport")
        for v in loco:
            if v not in ALLOWED_LOCO:
                errs.append(f"locomotion contains invalid {v}")
        turn = co.get("turning") or []
        if not isinstance(turn, list) or len(turn) < 2:
            errs.append("comfort_options.turning must have >=2 options")

    cp = obj.get("captions_policy")
    if not isinstance(cp, dict):
        errs.append("captions_policy missing")
    else:
        if cp.get("default_anchor") != "head-locked":
            errs.append("captions_policy.default_anchor must be head-locked")
        if cp.get("world_locked_available") is not True:
            errs.append("captions_policy.world_locked_available must be true")
        if cp.get("audio_descriptions") is not True:
            errs.append("captions_policy.audio_descriptions must be true")

    tm = obj.get("tester_mix")
    if not isinstance(tm, dict):
        errs.append("tester_mix missing")
    else:
        for k in ("low_vision", "motor_impaired", "motion_sensitive"):
            v = tm.get(k)
            if not isinstance(v, int) or v < 1:
                errs.append(f"tester_mix.{k} must be int >= 1")

    return errs


OK = {
    "__faion_header__": {"methodology": "spatial-accessibility", "version": "1.1.0", "produces": "report"},
    "platform": "visionos",
    "interactions": [{"name": "x", "primary_modality": "gaze+dwell", "alternative_modalities": ["voice"], "seated_compatible": True, "non_spatial_fallback": "flat"}],
    "comfort_options": {"locomotion": ["vignette", "teleport"], "turning": ["snap", "smooth"]},
    "captions_policy": {"default_anchor": "head-locked", "world_locked_available": True, "audio_descriptions": True},
    "tester_mix": {"low_vision": 1, "motor_impaired": 1, "motion_sensitive": 1},
}
BAD = {"platform": "quest", "interactions": [], "comfort_options": {"locomotion": ["smooth"], "turning": ["snap"]}}


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
