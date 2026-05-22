#!/usr/bin/env python3
"""validate-langchain-chains.py

Purpose:
    Validate a chain config envelope: pattern is one of four canonical values,
    module_level is true, fallback pattern has non-empty exceptions_to_handle.

Inputs:
    --file PATH      Chain config JSON
    --self-test      Validate the built-in smoke fixture

Outputs:
    Stdout: validation report
    Exit 0 on pass, 1 on failure, 2 on usage error.

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PATTERNS = {"sequential", "router", "map_reduce", "fallback"}
HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    pattern = obj.get("pattern")
    if pattern not in PATTERNS:
        errs.append(f"pattern: {pattern!r} not in {sorted(PATTERNS)}")
    if not isinstance(obj.get("module_level"), bool):
        errs.append("module_level: must be boolean")
    if obj.get("module_level") is False:
        errs.append("module_level: must be true (per r2-module-level-chains)")
    exc = obj.get("exceptions_to_handle")
    if not isinstance(exc, list):
        errs.append("exceptions_to_handle: must be list")
    elif pattern == "fallback" and not exc:
        errs.append("exceptions_to_handle: required non-empty when pattern=fallback")
    return errs


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--file", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    target = SMOKE if args.self_test else args.file
    if target is None:
        p.error("either --file or --self-test must be given")
    if not target.exists():
        sys.stdout.write(f"FAIL: file not found: {target}\n")
        return 1
    obj = json.loads(target.read_text(encoding="utf-8"))
    obj = {k: v for k, v in obj.items() if not k.startswith("_")}
    errs = validate(obj)
    if errs:
        sys.stdout.write(f"FAIL: {target}\n")
        for e in errs:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write(f"OK: {target}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
