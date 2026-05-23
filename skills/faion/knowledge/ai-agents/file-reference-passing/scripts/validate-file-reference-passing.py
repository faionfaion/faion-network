#!/usr/bin/env python3
"""validate-file-reference-passing.py

Purpose:
    Validate a ScanResult JSON against the schema in content/02-output-contract.xml.
    Checks rationale length and that every ref matches the kind:path pattern.

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

REF_RE = re.compile(r"^(path|db|gh|http|https):[^\s]+$")
HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    rationale = obj.get("rationale")
    if not isinstance(rationale, str) or not (4 <= len(rationale) <= 400):
        errs.append("rationale: must be 4-400 char string")
    refs = obj.get("relevant_refs")
    if not isinstance(refs, list):
        errs.append("relevant_refs: must be list")
        return errs
    for i, r in enumerate(refs):
        if not isinstance(r, str) or not REF_RE.match(r):
            errs.append(f"relevant_refs[{i}]: {r!r} does not match kind:path pattern")
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
