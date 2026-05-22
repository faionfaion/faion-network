#!/usr/bin/env python3
"""validate-field-descriptions-as-prompts.py

Purpose:
    Validate an audit-report JSON against the schema in content/02-output-contract.xml.
    Each issue must name the field and have a `kind` from the canonical enum.

Inputs:
    --file PATH      Audit-report JSON
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

KIND = {"missing", "duplicate-of-name", "asks-reasoning", "contradicts-type", "too-vague"}
HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.json"


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj.get("schema_id"), str):
        errs.append("schema_id: required string missing")
    fa = obj.get("fields_audited")
    if not isinstance(fa, int) or fa < 0:
        errs.append("fields_audited: required non-negative int")
    issues = obj.get("issues")
    if not isinstance(issues, list):
        errs.append("issues: must be a list")
        return errs
    for i, iss in enumerate(issues):
        if not isinstance(iss, dict):
            errs.append(f"issues[{i}]: must be an object")
            continue
        if not iss.get("field"):
            errs.append(f"issues[{i}].field: missing")
        if iss.get("kind") not in KIND:
            errs.append(f"issues[{i}].kind: {iss.get('kind')!r} not in {sorted(KIND)}")
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
