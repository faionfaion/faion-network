#!/usr/bin/env python3
"""validate-confidence-thresholded-cascade.py

Purpose:
    Validate a cheap-model output JSON against the cascade output contract
    (content/02-output-contract.xml). Confirms reasoning is present, the
    confidence field is named correctly, and requires_escalation is set.

Inputs:
    --file PATH      JSON file with the cheap-model output
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

REQUIRED = {"reasoning", "answer", "confidence_0_to_1", "requires_escalation"}

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.py"


def validate_cheap_answer(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root is not an object"]
    extra = set(obj.keys()) - REQUIRED
    if extra:
        errs.append(f"unexpected keys: {sorted(extra)}")
    missing = REQUIRED - set(obj.keys())
    if missing:
        errs.append(f"missing keys: {sorted(missing)}")
    r = obj.get("reasoning")
    if not isinstance(r, str) or len(r) < 4:
        errs.append("reasoning: must be non-empty string")
    c = obj.get("confidence_0_to_1")
    if not isinstance(c, (int, float)) or not (0.0 <= c <= 1.0):
        errs.append("confidence_0_to_1: must be a number in [0,1]")
    if not isinstance(obj.get("requires_escalation"), bool):
        errs.append("requires_escalation: must be boolean")
    if "confidence" in obj:
        errs.append("forbidden alias 'confidence' present; use 'confidence_0_to_1'")
    return errs


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--file", type=Path, help="JSON file with the cheap-model output")
    p.add_argument("--self-test", action="store_true", help="Validate the built-in smoke fixture")
    args = p.parse_args(argv)

    if not args.file and not args.self_test:
        p.error("either --file or --self-test must be given")

    if args.self_test:
        fixture = {
            "reasoning": "Smoke fixture for self-test.",
            "answer": "ok",
            "confidence_0_to_1": 0.92,
            "requires_escalation": False,
        }
        obj = fixture
        label = "<self-test fixture>"
    else:
        if not args.file.exists():
            sys.stdout.write(f"FAIL: file not found: {args.file}\n")
            return 1
        obj = json.loads(args.file.read_text(encoding="utf-8"))
        label = str(args.file)

    errs = validate_cheap_answer(obj)
    if errs:
        sys.stdout.write(f"FAIL: {label}\n")
        for e in errs:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write(f"OK: {label}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
