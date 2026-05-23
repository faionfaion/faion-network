#!/usr/bin/env python3
"""validate-ba-standup-script-template.py

Validate a BA standup script against 02-output-contract.xml.

Inputs:
    --file PATH       path to script JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid; 1 = invalid; 2 = usage / unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEV = {"low", "medium", "high"}
ANON = {"team", "we", "us", "ops", "?", ""}


def _anon(name: str) -> bool:
    n = (name or "").strip().lower()
    return not n or n in ANON or len(n.split()) < 2


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("date", "ba_name", "clarifications_needed", "ac_ready_for_dev", "blockers"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if not ISO_DATE.match(obj.get("date", "")):
        errs.append("date must be YYYY-MM-DD (rule r4)")
    for i, c in enumerate(obj.get("clarifications_needed", [])):
        if not c.get("story_id") or len(c.get("question", "")) < 8 or _anon(c.get("stakeholder", "")):
            errs.append(f"clarifications_needed[{i}] missing story_id/question/stakeholder (rule r2)")
    for i, a in enumerate(obj.get("ac_ready_for_dev", [])):
        if not a.get("story_id") or a.get("ac_count", 0) < 1:
            errs.append(f"ac_ready_for_dev[{i}] missing story_id or ac_count (rule r2)")
    for i, b in enumerate(obj.get("blockers", [])):
        if _anon(b.get("owner", "")):
            errs.append(f"blockers[{i}].owner anonymous '{b.get('owner')}' (rule r3)")
        if len(b.get("description", "")) < 8:
            errs.append(f"blockers[{i}].description too short (rule r2)")
        if b.get("severity") and b["severity"] not in SEV:
            errs.append(f"blockers[{i}].severity must be one of {sorted(SEV)}")
    return errs


OK_FIXTURE = {
    "date": "2026-05-23", "ba_name": "Maria Lopes",
    "clarifications_needed": [{"story_id": "S-1", "question": "Refund window?", "stakeholder": "Pedro Silva"}],
    "ac_ready_for_dev": [{"story_id": "S-2", "ac_count": 3}],
    "blockers": [{"description": "DPO pending classification", "owner": "Ana Rodrigues", "raised_at": "2026-05-22T10:00:00Z", "severity": "high"}],
}
BAD_FIXTURE = {"date": "x", "ba_name": "x", "clarifications_needed": [{"story_id": "", "question": "?", "stakeholder": "team"}],
               "ac_ready_for_dev": [], "blockers": [{"description": "x", "owner": "we"}]}


def self_test() -> int:
    if validate(OK_FIXTURE):
        sys.stderr.write("OK rejected\n"); return 1
    if not validate(BAD_FIXTURE):
        sys.stderr.write("BAD accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n"); return 0


if __name__ == "__main__":
    sys.exit(main())
