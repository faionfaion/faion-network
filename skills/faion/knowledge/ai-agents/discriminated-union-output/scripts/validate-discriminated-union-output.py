#!/usr/bin/env python3
"""validate-discriminated-union-output.py

Purpose:
    Validate an action JSON against the discriminated-union contract declared
    in content/02-output-contract.xml. Confirms the `kind` discriminator is
    present and that the per-branch required fields match.

Inputs:
    --file PATH      Action JSON
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

BRANCH_REQUIRED = {
    "search":   {"kind", "query"},
    "fetch":    {"kind", "url"},
    "ask_user": {"kind", "question"},
    "finish":   {"kind", "summary"},
}

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root is not an object"]
    kind = obj.get("kind")
    if kind not in BRANCH_REQUIRED:
        errs.append(f"kind: {kind!r} not in {sorted(BRANCH_REQUIRED)}")
        return errs
    required = BRANCH_REQUIRED[kind]
    extra = set(obj.keys()) - required
    if extra:
        errs.append(f"unexpected fields for kind={kind}: {sorted(extra)}")
    missing = required - set(obj.keys())
    if missing:
        errs.append(f"missing fields for kind={kind}: {sorted(missing)}")
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
    sys.stdout.write(f"OK: {target} (kind={obj['kind']})\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
