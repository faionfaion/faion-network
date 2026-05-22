#!/usr/bin/env python3
"""validate-decimal-as-string-pattern.py

Purpose:
    Validate a JSON line-item document against the patterned-string contract
    declared in content/02-output-contract.xml: SKU pattern, integer quantity,
    decimal-string unit_price_usd with two decimals.

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
import re
import sys
from pathlib import Path

SKU_RE = re.compile(r"^[A-Z0-9-]{2,40}$")
PRICE_RE = re.compile(r"^\d+\.\d{2}$")

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root is not an object"]
    sku = obj.get("sku")
    if not isinstance(sku, str) or not SKU_RE.match(sku):
        errs.append(f"sku: {sku!r} does not match {SKU_RE.pattern}")
    q = obj.get("quantity")
    if not isinstance(q, int) or q < 1 or q > 10_000:
        errs.append("quantity: must be integer in [1, 10000]")
    price = obj.get("unit_price_usd")
    if not isinstance(price, str) or not PRICE_RE.match(price):
        errs.append(f"unit_price_usd: {price!r} does not match {PRICE_RE.pattern}")
    if isinstance(price, float):
        errs.append("unit_price_usd: must be string, not float (drift risk)")
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
    # Strip helper keys
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
