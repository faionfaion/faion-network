#!/usr/bin/env python3
"""validate-internal-link-audit.py

Validates a report artefact produced by methodology 'internal-link-audit' against the
JSON Schema embedded in content/02-output-contract.xml.

Inputs:
    --file PATH       artefact JSON path
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["slug", "owner", "period_start", "period_end", "metrics", "findings", "deviation_log_reference"]


def validate(obj) -> list:
    errs: list = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "slug" in obj and obj["slug"] != "internal-link-audit":
        errs.append(f"slug must equal 'internal-link-audit'")
    if "metrics" in obj and (not isinstance(obj["metrics"], list) or len(obj["metrics"]) < 1):
        errs.append("metrics must be array with >=1 items")
    if "findings" in obj and (not isinstance(obj["findings"], list) or len(obj["findings"]) < 1):
        errs.append("findings must be array with >=1 items")
    serialised = json.dumps(obj)
    for marker in ("TBD", "TODO", "FIXME"):
        if marker in serialised:
            errs.append(f"forbidden token in payload: {marker}")
    return errs


FIXTURE_OK = {"slug": "internal-link-audit", "owner": "analytics owner", "period_start": "2026-05-01", "period_end": "2026-05-22", "metrics": [{"name": "activation_rate", "value": 0.31, "unit": "ratio"}], "findings": ["activation rate up 4pp WoW; biggest lift from onboarding checklist v2"], "deviation_log_reference": "ops/deviation-log.md#L88"}


def self_test() -> int:
    errs = validate(FIXTURE_OK)
    if errs:
        for e in errs:
            sys.stderr.write(f"self-test fixture rejected: {e}\n")
        return 1
    errs2 = validate({"slug": "internal-link-audit"})
    if not errs2:
        sys.stderr.write("self-test: deliberately-broken fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
