#!/usr/bin/env python3
"""validate-filesystem-as-working-memory.py

Purpose:
    Validate an offloaded-envelope JSON: path is under canonical taxonomy,
    head is at most 800 chars, kind is "offloaded".

Inputs:
    --file PATH      JSON to validate
    --self-test      Validate the built-in smoke fixture

Outputs:
    Stdout: validation report
    Exit 0 on pass, 1 on failure, 2 on usage error.

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PATH_RE = re.compile(r"^(search|docs|plan|scratch)/[^\s]+$")
HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if obj.get("kind") != "offloaded":
        errs.append(f"kind: must be 'offloaded'; got {obj.get('kind')!r}")
    p = obj.get("path")
    if not isinstance(p, str) or not PATH_RE.match(p):
        errs.append(f"path: {p!r} not under canonical taxonomy")
    h = obj.get("head")
    if not isinstance(h, str) or len(h) > 800:
        errs.append("head: must be string <= 800 chars")
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
