#!/usr/bin/env python3
"""validate-best-practices-2026.py — Validate the best-practices-2026 constitution-snapshot record.

Inputs: <record.json>

Outputs: stdout PASS/FAIL with violations.

Exit codes: 0 pass, 1 fail, 2 usage.

Flags:
  --help        Show this message.
  --self-test   Run against a built-in fixture.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
RULE_RE = re.compile(r"^r[0-9]+-[a-z-]+$")
DRIFT_WINDOW_DAYS = 90

VALID = {
    "snapshot_version": "1.1.0",
    "stack": {"python": "3.12"},
    "extracted_rules": ["r1-match-tool-to-task"],
    "drift_scan_date": dt.date.today().isoformat(),
}
INVALID = {"snapshot_version": "latest", "extracted_rules": [], "drift_scan_date": "soon"}


def validate(rec: dict) -> list[str]:
    out: list[str] = []
    for k in ("snapshot_version", "extracted_rules", "drift_scan_date"):
        if k not in rec:
            out.append(f"missing {k}")
    if out:
        return out
    if not SEMVER_RE.match(str(rec["snapshot_version"])):
        out.append("snapshot_version must be semver")
    if not isinstance(rec["extracted_rules"], list) or not rec["extracted_rules"]:
        out.append("extracted_rules must be non-empty list")
    else:
        for r in rec["extracted_rules"]:
            if not RULE_RE.match(str(r)):
                out.append(f"rule id invalid: {r!r}")
    try:
        d = dt.date.fromisoformat(str(rec["drift_scan_date"]))
        age = (dt.date.today() - d).days
        if age > DRIFT_WINDOW_DAYS:
            out.append(f"drift_scan_date stale ({age} days; max {DRIFT_WINDOW_DAYS})")
    except ValueError:
        out.append("drift_scan_date must be ISO date")
    if "stack" not in rec or not isinstance(rec["stack"], dict):
        out.append("stack must be object")
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[1] in ("--help", "-h"):
        sys.stdout.write(__doc__ or "")
        return 0 if "--help" in argv else 2
    if argv[1] == "--self-test":
        ok = validate(VALID)
        bad = validate(INVALID)
        if ok:
            sys.stderr.write(f"self-test FAIL: valid rejected: {ok}\n")
            return 1
        if not bad:
            sys.stderr.write("self-test FAIL: invalid accepted\n")
            return 1
        sys.stdout.write("self-test OK\n")
        return 0
    p = Path(argv[1])
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        rec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"invalid JSON: {exc}\n")
        return 1
    v = validate(rec)
    if v:
        sys.stdout.write("FAIL\n")
        for x in v:
            sys.stdout.write(f"  - {x}\n")
        return 1
    sys.stdout.write("PASS\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
