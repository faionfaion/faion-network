#!/usr/bin/env python3
"""validate-agent-failure-taxonomy.py — validate output artefacts against the agent-failure-taxonomy output contract.

Inputs:
  - path to a JSON file produced by the methodology

Outputs:
  - stdout: human-readable violation list (empty on pass)
  - exit 0 on pass, 1 on fail

Exit codes:
  0 — valid
  1 — schema violations
  2 — usage error
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ['labels', 'primary_label_per_instance', 'history_log', 'owner', 'version', 'forbidden_seen']
FORBIDDEN_KEYS = ['f1', 'f2', 'f3', 'f4']


def validate(doc: dict) -> list[str]:
    errs: list[str] = []
    for k in REQUIRED:
        if k not in doc:
            errs.append(f"missing required field: {k}")
    fs = doc.get("forbidden_seen", None)
    if fs is None:
        errs.append("missing forbidden_seen array (required)")
    elif not isinstance(fs, list):
        errs.append("forbidden_seen must be an array")
    elif len(fs) > 0:
        errs.append(f"forbidden_seen non-empty: {fs}")
    return errs


SMOKE = {k: ("example" if k != "forbidden_seen" else []) for k in REQUIRED + ["forbidden_seen"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate agent-failure-taxonomy output JSON.")
    parser.add_argument("path", nargs="?", help="Path to JSON output to validate.")
    parser.add_argument("--self-test", action="store_true", help="Run an in-process smoke test with a built-in fixture.")
    args = parser.parse_args()

    if args.self_test:
        errs = validate(SMOKE)
        if errs:
            print("self-test failed:", errs, file=sys.stderr)
            return 1
        print("self-test ok")
        return 0

    if not args.path:
        parser.print_help()
        return 2

    p = Path(args.path)
    if not p.exists():
        print(f"file not found: {p}", file=sys.stderr)
        return 2

    try:
        doc = json.loads(p.read_text())
    except Exception as e:
        print(f"json parse error: {e}", file=sys.stderr)
        return 1

    errs = validate(doc)
    if errs:
        for e in errs:
            print(e)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
