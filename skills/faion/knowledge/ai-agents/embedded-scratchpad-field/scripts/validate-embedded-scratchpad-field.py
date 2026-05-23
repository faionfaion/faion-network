#!/usr/bin/env python3
"""validate-embedded-scratchpad-field.py

Purpose:
    Validate a verdict-style JSON against the schema in content/02-output-contract.xml.
    Confirms reasoning is present, non-empty, and reasonably long; confidence is enum;
    decision is enum.

Inputs:
    --file PATH      Verdict JSON
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

CONFIDENCE = {"low", "medium", "high"}
DECISION = {"approve", "reject"}

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root is not an object"]
    keys = [k for k in obj.keys() if not k.startswith("_")]
    if keys[:1] != ["reasoning"]:
        errs.append(f"reasoning must be the FIRST key; got order {keys}")
    r = obj.get("reasoning")
    if not isinstance(r, str) or len(r) < 4:
        errs.append("reasoning: must be non-empty string >= 4 chars")
    c = obj.get("confidence")
    if c not in CONFIDENCE:
        errs.append(f"confidence: {c!r} not in {sorted(CONFIDENCE)}")
    d = obj.get("decision")
    if d not in DECISION:
        errs.append(f"decision: {d!r} not in {sorted(DECISION)}")
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
