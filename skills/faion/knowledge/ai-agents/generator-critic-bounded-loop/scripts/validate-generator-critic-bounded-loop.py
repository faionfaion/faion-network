#!/usr/bin/env python3
"""validate-generator-critic-bounded-loop.py

Purpose:
    Validate a critic output JSON against the schema in content/02-output-contract.xml:
    score in [0,1], should_continue is bool, feedback non-empty.

Inputs:
    --file PATH      Critic output JSON
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

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    s = obj.get("score")
    if not isinstance(s, (int, float)) or not (0.0 <= s <= 1.0):
        errs.append(f"score: {s!r} not in [0,1]")
    if not isinstance(obj.get("should_continue"), bool):
        errs.append("should_continue: must be boolean")
    fb = obj.get("feedback")
    if not isinstance(fb, str) or len(fb) < 4:
        errs.append("feedback: must be non-empty string")
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
