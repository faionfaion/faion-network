#!/usr/bin/env python3
"""validate-banking-core-data-residency-rules.py — validate output artefacts against the banking-core-data-residency-rules output contract.

Inputs:
  - path to a JSON file produced by the methodology

Outputs:
  - stdout: human-readable violation list (empty on pass)
  - exit 0 on pass, 1 on fail, 2 on usage error

Exit codes:
  0 -- valid
  1 -- schema violations
  2 -- usage error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["jurisdictions", "data_classes", "processors", "transfers", "notification_triggers"]
FORBIDDEN_IDS = ["f1", "f2", "f3"]


def validate(doc: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(doc, dict):
        errs.append("payload must be a JSON object")
        return errs
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing required field: {k}")
    fs = doc.get("forbidden_seen")
    if isinstance(fs, list) and len(fs) > 0:
        errs.append(f"forbidden_seen non-empty: {fs}")
    return errs


SMOKE = {k: ("example" if k != "forbidden_seen" else []) for k in REQUIRED}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate banking-core-data-residency-rules output JSON.")
    parser.add_argument("path", nargs="?", help="Path to JSON output to validate.")
    parser.add_argument("--self-test", action="store_true", help="Run an in-process smoke test with a built-in fixture.")
    args = parser.parse_args()

    if args.self_test:
        errs = validate(SMOKE)
        if errs:
            sys.stderr.write("self-test failed: " + repr(errs) + "\n")
            return 1
        sys.stdout.write("self-test ok\n")
        return 0

    if not args.path:
        parser.print_help()
        return 2

    p = Path(args.path)
    if not p.exists():
        sys.stderr.write(f"file not found: {p}\n")
        return 2

    try:
        doc = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"json parse error: {e}\n")
        return 1

    errs = validate(doc)
    if errs:
        for e in errs:
            sys.stdout.write(e + "\n")
        return 1
    sys.stdout.write("ok\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
