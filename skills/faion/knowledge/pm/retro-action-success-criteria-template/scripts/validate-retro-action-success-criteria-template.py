#!/usr/bin/env python3
"""validate-retro-action-success-criteria-template.py

Validate a RetroActionItem JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to actions JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

SPRINT_RX = re.compile(r"^S[0-9]+$")
VERDICTS = {"pending", "met", "missed", "abandoned"}
BAD_PHRASES = ("communicate better", "improve handoffs", "be better", "feels good")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("sprint_id", "header", "actions"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    if not SPRINT_RX.match(obj["sprint_id"]):
        errs.append("sprint_id must match ^S[0-9]+$")
    h = obj["header"]
    if not h.get("owner", {}).get("person"):
        errs.append("header.owner.person empty")
    lr = h.get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
        if (dt.date.today() - d).days > 90:
            errs.append(f"header.last_reviewed {lr} > 90 days (rule: r3-version-and-owner)")
    except Exception:
        errs.append("header.last_reviewed not ISO date")

    for i, a in enumerate(obj["actions"]):
        exp = a.get("experiment", "")
        if len(exp) < 20:
            errs.append(f"actions[{i}].experiment too short (rule: r1-fixed-shape)")
        for bp in BAD_PHRASES:
            if bp in exp.lower():
                errs.append(f"actions[{i}].experiment contains vague phrase '{bp}'")
        if len(a.get("threshold", "")) < 5:
            errs.append(f"actions[{i}].threshold too vague (rule: r2-evidence-fields)")
        if a.get("owner_role", "").lower() in {"team", ""}:
            errs.append(f"actions[{i}].owner_role too vague (rule: r3-version-and-owner)")
        if not SPRINT_RX.match(str(a.get("deadline_sprint", ""))):
            errs.append(f"actions[{i}].deadline_sprint must match ^S[0-9]+$")
        if a.get("outcome_verdict") not in VERDICTS:
            errs.append(f"actions[{i}].outcome_verdict invalid")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "sprint_id": "S14",
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01", "version": "0"},
    "actions": [{"action_id": "x", "experiment": "communicate better", "input_signal": "",
                 "measurement_source": "", "threshold": "feels good",
                 "deadline_sprint": "soon", "owner_role": "team", "outcome_verdict": "pending"}]
}


def self_test() -> int:
    if SMOKE_OK_FILE.is_file():
        ok = json.loads(SMOKE_OK_FILE.read_text())
        ok["header"]["last_reviewed"] = dt.date.today().isoformat()
        errs = validate(ok)
        if errs:
            sys.stderr.write("smoke_ok rejected: " + "; ".join(errs) + "\n"); return 1
    if not validate(SMOKE_BAD):
        sys.stderr.write("smoke_bad accepted\n"); return 1
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
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
