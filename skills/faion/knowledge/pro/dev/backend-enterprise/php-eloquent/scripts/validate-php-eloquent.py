#!/usr/bin/env python3
"""validate-php-eloquent.py

Validate the Eloquent-discipline manifest for the php-eloquent methodology
against the JSON Schema declared in 02-output-contract.xml.

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

REQUIRED = ["laravel_version", "models", "prevent_lazy_loading_enabled", "paired_artefacts"]
LARAVEL_RE = re.compile(r"^(10|11)\.")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not LARAVEL_RE.match(str(obj.get("laravel_version", ""))):
        errs.append("laravel_version must be 10.x or 11.x")
    models = obj.get("models") or []
    if not isinstance(models, list) or len(models) < 1:
        errs.append("models must be non-empty list")
    for i, m in enumerate(models):
        if m.get("uses_fillable") is not True:
            errs.append(f"models[{i}].uses_fillable must be true")
        if m.get("uses_attribute_make") is not True:
            errs.append(f"models[{i}].uses_attribute_make must be true")
        if m.get("uses_guarded_empty") is not False:
            errs.append(f"models[{i}].uses_guarded_empty must be false")
    if obj.get("prevent_lazy_loading_enabled") is not True:
        errs.append("prevent_lazy_loading_enabled must be true")
    pa = obj.get("paired_artefacts") or {}
    for k in ("migration", "factory", "resource"):
        if pa.get(k) is not True:
            errs.append(f"paired_artefacts.{k} must be true")
    forbidden = obj.get("forbidden_patterns_found") or []
    if forbidden:
        errs.append(f"forbidden_patterns_found must be empty, got {forbidden}")
    return errs


OK = {
    "laravel_version": "11.0",
    "models": [{"class": "App\\Models\\User", "uses_fillable": True, "uses_attribute_make": True, "uses_guarded_empty": False}],
    "prevent_lazy_loading_enabled": True,
    "paired_artefacts": {"migration": True, "factory": True, "resource": True},
    "forbidden_patterns_found": [],
}
BAD = {
    "laravel_version": "8.0",
    "models": [{"class": "User", "uses_fillable": False, "uses_attribute_make": False, "uses_guarded_empty": True}],
    "prevent_lazy_loading_enabled": False,
    "paired_artefacts": {"migration": False, "factory": False, "resource": False},
    "forbidden_patterns_found": ["$guarded = []"],
}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok fixture rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
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
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
