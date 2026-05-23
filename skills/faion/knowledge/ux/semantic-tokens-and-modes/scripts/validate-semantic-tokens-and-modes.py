#!/usr/bin/env python3
"""validate-semantic-tokens-and-modes.py

Validate a token-config artefact against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to token-config JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
ALLOWED_MODES = {"light", "dark", "high-contrast", "compact", "comfortable", "brand-a", "brand-b", "white-label"}
ALLOWED_TYPES = {"color", "dimension", "fontFamily", "fontWeight", "duration", "cubicBezier", "shadow"}
ALLOWED_BUILDERS = {"style-dictionary", "tokens-studio", "specify"}
ALLOWED_PLATFORMS = {"css", "swift", "compose", "android-xml"}
ALLOWED_VR_TOOLS = {"chromatic", "percy", "loki"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]

    hdr = obj.get("__faion_header__")
    if not isinstance(hdr, dict):
        errs.append("missing __faion_header__ object")
    else:
        if hdr.get("methodology") != "semantic-tokens-and-modes":
            errs.append("__faion_header__.methodology must be 'semantic-tokens-and-modes'")
        if not VER_RE.match(str(hdr.get("version", ""))):
            errs.append("__faion_header__.version must be semver")
        if hdr.get("produces") != "config":
            errs.append("__faion_header__.produces must be 'config'")

    if obj.get("format") != "dtcg":
        errs.append("format must be 'dtcg'")

    layers = obj.get("layers") or {}
    for k in ("reference", "system", "component"):
        if layers.get(k) is not True:
            errs.append(f"layers.{k} must be true")

    modes = obj.get("modes")
    if not isinstance(modes, list) or not modes:
        errs.append("modes must be non-empty list")
    else:
        for m in modes:
            if m not in ALLOWED_MODES:
                errs.append(f"modes contains invalid value: {m}")

    tokens = obj.get("tokens") or {}
    system = tokens.get("system")
    if not isinstance(system, dict):
        errs.append("tokens.system must be object")
    elif isinstance(modes, list) and modes:
        for name, tok in system.items():
            if "$type" not in tok or tok["$type"] not in ALLOWED_TYPES:
                errs.append(f"tokens.system.{name}.$type missing or invalid")
            vbm = tok.get("values_by_mode") or {}
            if not isinstance(vbm, dict):
                errs.append(f"tokens.system.{name}.values_by_mode must be object")
                continue
            for m in modes:
                if m not in vbm:
                    errs.append(f"tokens.system.{name}.values_by_mode missing mode {m}")

    pipeline = obj.get("pipeline") or {}
    if pipeline.get("builder") not in ALLOWED_BUILDERS:
        errs.append("pipeline.builder invalid")
    plats = pipeline.get("platforms")
    if not isinstance(plats, list) or not plats:
        errs.append("pipeline.platforms must be non-empty list")
    else:
        for p in plats:
            if p not in ALLOWED_PLATFORMS:
                errs.append(f"pipeline.platforms invalid: {p}")

    vr = obj.get("visual_regression")
    if isinstance(vr, dict):
        if vr.get("tool") not in ALLOWED_VR_TOOLS:
            errs.append("visual_regression.tool invalid")
        if vr.get("snapshot_every_mode") is not True:
            errs.append("visual_regression.snapshot_every_mode must be true")

    return errs


OK = {
    "__faion_header__": {"methodology": "semantic-tokens-and-modes", "version": "1.1.0", "produces": "config"},
    "format": "dtcg",
    "layers": {"reference": True, "system": True, "component": True},
    "modes": ["light", "dark"],
    "tokens": {"system": {"color.action.primary": {"$type": "color", "values_by_mode": {"light": "{color.blue.600}", "dark": "{color.blue.400}"}}}},
    "pipeline": {"builder": "style-dictionary", "platforms": ["css"]},
    "visual_regression": {"tool": "chromatic", "snapshot_every_mode": True},
}
BAD = {"format": "internal-json", "modes": [], "tokens": {"system": {}}}


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
