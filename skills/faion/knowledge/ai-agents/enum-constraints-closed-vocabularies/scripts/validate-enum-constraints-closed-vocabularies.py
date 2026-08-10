#!/usr/bin/env python3
"""validate-enum-constraints-closed-vocabularies.py

Purpose:
    Validate a ticket JSON against the enum value sets declared in
    content/02-output-contract.xml.

Inputs:
    --file PATH      JSON file to validate
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

CATEGORY = {"billing", "tech_support", "refund", "spam", "other"}
PRIORITY = {"P0", "P1", "P2", "P3"}
SENTIMENT = {"angry", "frustrated", "neutral", "happy"}

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root is not an object"]
    if obj.get("category") not in CATEGORY:
        errs.append(f"category: {obj.get('category')!r} not in {sorted(CATEGORY)}")
    if obj.get("priority") not in PRIORITY:
        errs.append(f"priority: {obj.get('priority')!r} not in {sorted(PRIORITY)}")
    if obj.get("sentiment") not in SENTIMENT:
        errs.append(f"sentiment: {obj.get('sentiment')!r} not in {sorted(SENTIMENT)}")
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
