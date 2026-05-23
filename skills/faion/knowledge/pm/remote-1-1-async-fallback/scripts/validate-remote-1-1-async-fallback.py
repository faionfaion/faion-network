#!/usr/bin/env python3
"""validate-remote-1-1-async-fallback.py

Validate an Async11Note JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to note JSON
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

WEEK_RX = re.compile(r"^[0-9]{4}-W[0-9]{2}$")
ESC = {"none", "synchronous_reschedule", "escalate_to_manager"}
SPRINT_RX = re.compile(r"^S[0-9]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("pair_id", "cycle_iso", "header", "prompts", "ic_response", "pm_ack", "escalation"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    if not obj["pair_id"]:
        errs.append("pair_id empty")
    if not WEEK_RX.match(obj["cycle_iso"]):
        errs.append("cycle_iso must match YYYY-Www")
    h = obj["header"]
    if not h.get("owner", {}).get("person"):
        errs.append("header.owner.person empty (rule: r4-named-owner)")
    rw = h.get("response_window_business_hours", 0)
    if not (24 <= rw <= 168):
        errs.append("header.response_window_business_hours outside [24,168]")
    lr = h.get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
        if (dt.date.today() - d).days > 90:
            errs.append(f"header.last_reviewed {lr} > 90 days (rule: r5-iteration-loop)")
    except Exception:
        errs.append("header.last_reviewed not ISO date")

    for k in ("blockers", "decisions_needed", "morale"):
        if len(obj["prompts"].get(k, "")) < 10:
            errs.append(f"prompts.{k} too short (rule: r2-bounded-output)")

    esc = obj["escalation"]
    if esc.get("action") not in ESC:
        errs.append("escalation.action invalid")
    if esc.get("unresponsive_count", 0) >= 2 and esc.get("action") == "none":
        errs.append("unresponsive_count >= 2 with action=none (rule: r1-explicit-trigger)")

    for i, na in enumerate(obj["pm_ack"].get("next_actions", [])):
        if not SPRINT_RX.match(str(na.get("deadline_sprint", ""))):
            errs.append(f"pm_ack.next_actions[{i}].deadline_sprint must match ^S[0-9]+$ (rule: r4-named-owner)")
        if not na.get("owner_role"):
            errs.append(f"pm_ack.next_actions[{i}].owner_role empty")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "pair_id": "x", "cycle_iso": "2026-W21",
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01",
               "version": "0", "response_window_business_hours": 12},
    "prompts": {"blockers": "?", "decisions_needed": "?", "morale": "?"},
    "ic_response": {"received_at": None, "blockers": "", "decisions_needed": "", "morale": ""},
    "pm_ack": {"acked_at": None, "next_actions": []},
    "escalation": {"unresponsive_count": 3, "action": "none"}
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
