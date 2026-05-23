#!/usr/bin/env python3
"""validate-shadow-handover-session-runbook.py

Validate a HandoverSessionRecord JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to record JSON
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
import sys
from pathlib import Path

VERDICTS = {"unaided", "needs_second_session", "deferred", "spf_undocumented"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("session_id", "header", "task_list", "gap_log", "sign_off"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    h = obj["header"]
    if not h.get("outgoing_engineer") or not h.get("receiver"):
        errs.append("header.outgoing_engineer/receiver empty")
    if not h.get("owner", {}).get("person"):
        errs.append("header.owner.person empty")
    lr = h.get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
        if (dt.date.today() - d).days > 90:
            errs.append(f"header.last_reviewed {lr} > 90 days")
    except Exception:
        errs.append("header.last_reviewed not ISO date")

    if not obj["task_list"]:
        errs.append("task_list empty (rule: r5-no-skipped-tasks)")
    for i, t in enumerate(obj["task_list"]):
        if t.get("verdict") not in VERDICTS:
            errs.append(f"task_list[{i}].verdict invalid")
        if not t.get("receiver_drove") and t.get("verdict") not in {"deferred", "spf_undocumented"}:
            errs.append(f"task_list[{i}] receiver_drove=false but verdict not deferred (rule: r1-receiver-drives)")

    so = obj["sign_off"]
    if not so.get("outgoing_signed_by") or not so.get("receiver_signed_by"):
        errs.append("sign_off requires both signatures (rule: r4-sign-off-gate)")

    for i, g in enumerate(obj["gap_log"]):
        if "doc_link" not in g:
            errs.append(f"gap_log[{i}].doc_link missing (rule: r3-written-gap-log; null means open action)")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "session_id": "x",
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01", "version": "0", "outgoing_engineer": "", "receiver": ""},
    "task_list": [{"task_id": "T1", "description": "x", "receiver_drove": False, "verdict": "unaided"}],
    "gap_log": [{"question": "where?", "answer": "ask", "doc_link": None}],
    "sign_off": {"outgoing_signed_by": "", "receiver_signed_by": "", "signed_at": "2026-05-20"}
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
