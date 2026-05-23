#!/usr/bin/env python3
"""validate-daily-ads-anomaly-checklist.py

Validate the daily-run log JSON against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to log JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BANNED_OWNER = re.compile(r"^(team|we|us)$", re.I)
CHECK_NAMES = {"spend_spike", "cpa_spike", "frequency_spike", "ctr_drop", "conversion_drop", "account_health"}
ACTIONS = {"no-op", "pause", "reduce-budget", "raise-budget", "escalate"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("run_date", "account_id", "checks", "owner"):
        if k not in obj:
            errs.append(f"missing required: {k}")
    owner = obj.get("owner", "")
    if not isinstance(owner, str) or len(owner) < 3:
        errs.append("owner missing or too short")
    elif BANNED_OWNER.match(owner.strip()):
        errs.append(f"owner is banned plural noun: {owner!r}")
    checks = obj.get("checks") or []
    if not isinstance(checks, list) or len(checks) < 6:
        errs.append("checks must be an array of all 6 anomaly types")
    seen = set()
    for i, c in enumerate(checks if isinstance(checks, list) else []):
        for k in ("check", "threshold", "actual", "tripped", "action"):
            if k not in c:
                errs.append(f"checks[{i}] missing: {k}")
        cn = c.get("check")
        if cn in CHECK_NAMES:
            seen.add(cn)
        else:
            errs.append(f"checks[{i}].check invalid: {cn!r}")
        a = c.get("action")
        if a not in ACTIONS:
            errs.append(f"checks[{i}].action invalid: {a!r}")
        if c.get("tripped") and a == "no-op":
            errs.append(f"checks[{i}] tripped=true with action=no-op (rule named-owner-action)")
        if a == "pause" and not c.get("auto_resume_at"):
            errs.append(f"checks[{i}] action=pause without auto_resume_at (rule reversible-pause-default)")
        if a == "escalate" and not c.get("escalation_thread"):
            errs.append(f"checks[{i}] action=escalate without escalation_thread")
    missing_checks = CHECK_NAMES - seen
    if missing_checks:
        errs.append(f"missing check categories: {sorted(missing_checks)}")
    return errs


OK = {
    "run_date": "2026-05-23",
    "account_id": "meta-act-123",
    "owner": "@alex-ppc",
    "checks": [
        {"check": "spend_spike", "threshold": "1.5x", "actual": "1.62x", "tripped": True, "action": "reduce-budget"},
        {"check": "cpa_spike", "threshold": 80, "actual": 142, "tripped": True, "action": "pause", "auto_resume_at": "2026-05-24T08:00:00Z"},
        {"check": "frequency_spike", "threshold": 4.0, "actual": 3.1, "tripped": False, "action": "no-op"},
        {"check": "ctr_drop", "threshold": "-30%", "actual": "-12%", "tripped": False, "action": "no-op"},
        {"check": "conversion_drop", "threshold": "-40%", "actual": "-45%", "tripped": True, "action": "escalate", "escalation_thread": "#x"},
        {"check": "account_health", "threshold": "no_warn", "actual": "1_warn", "tripped": True, "action": "escalate", "escalation_thread": "#x"},
    ],
}
BAD = {"run_date": "2026-05-23", "account_id": "x", "owner": "team", "checks": []}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write(f"ok rejected: {validate(OK)}\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
