#!/usr/bin/env python3
"""validate-idempotent-write-tools.py

Purpose:
    Validate a tool-call body for the apply contract: preview_hash matches
    sha256 pattern, idempotency_key matches the canonical pattern.

Inputs:
    --file PATH      Tool-call body JSON
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

HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
KEY_RE = re.compile(r"^[A-Za-z0-9._-]{8,128}$")
HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    ph = obj.get("preview_hash")
    if not isinstance(ph, str) or not HASH_RE.match(ph):
        errs.append(f"preview_hash: {ph!r} does not match sha256:<64hex>")
    key = obj.get("idempotency_key")
    if not isinstance(key, str) or not KEY_RE.match(key):
        errs.append(f"idempotency_key: {key!r} does not match canonical pattern")
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
