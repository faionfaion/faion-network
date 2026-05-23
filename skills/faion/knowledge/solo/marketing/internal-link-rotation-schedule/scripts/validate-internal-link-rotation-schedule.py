#!/usr/bin/env python3
"""validate-internal-link-rotation-schedule.py

Validate the rotation calendar + audit log + deferred-fix register bundle
against content/02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
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
from datetime import date
from pathlib import Path

QUARTER_RE = re.compile(r"^[0-9]{4}-Q[1-4]$")
SLOT_STATUSES = {"scheduled", "done", "paused"}
FIX_STATUSES = {"open", "done", "escalated"}


def _parse_date(s):
    try:
        y, m, d = s.split("-")
        return date(int(y), int(m), int(d))
    except Exception:
        return None


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("quarter", "rotation_calendar", "audit_log", "deferred_fixes", "retrospective"):
        if k not in obj:
            errs.append("missing required: " + k)
    q = obj.get("quarter", "")
    if not QUARTER_RE.match(str(q)):
        errs.append("quarter must match YYYY-Qn")
    rc = obj.get("rotation_calendar", [])
    if not isinstance(rc, list) or not (3 <= len(rc) <= 10):
        errs.append("rotation_calendar must have 3-10 entries")
    else:
        for i, slot in enumerate(rc):
            for k in ("slot_n", "scheduled_date", "cluster_id"):
                if k not in slot:
                    errs.append("rotation_calendar[" + str(i) + "] missing " + k)
            if slot.get("status") and slot["status"] not in SLOT_STATUSES:
                errs.append("rotation_calendar[" + str(i) + "] status not in enum")
    log = obj.get("audit_log", [])
    if isinstance(log, list):
        for i, row in enumerate(log):
            for k in ("slot_n", "cluster_id", "started_at", "duration_minutes",
                      "fixes_shipped", "fixes_deferred"):
                if k not in row:
                    errs.append("audit_log[" + str(i) + "] missing " + k)
            dur = row.get("duration_minutes")
            if isinstance(dur, int) and dur > 60:
                errs.append("audit_log[" + str(i) + "] duration_minutes > 60 (time-box overrun)")
    fixes = obj.get("deferred_fixes", [])
    if isinstance(fixes, list):
        for i, f in enumerate(fixes):
            for k in ("fix_id", "logged_at", "due_date", "cluster_id", "status"):
                if k not in f:
                    errs.append("deferred_fixes[" + str(i) + "] missing " + k)
            if f.get("status") and f["status"] not in FIX_STATUSES:
                errs.append("deferred_fixes[" + str(i) + "] status not in enum")
            la = _parse_date(f.get("logged_at", ""))
            dd = _parse_date(f.get("due_date", ""))
            if la and dd and (dd - la).days > 30:
                errs.append("deferred_fixes[" + str(i) + "] due_date - logged_at > 30 days (SLA exceeded)")
    return errs


OK = {
    "quarter": "2026-Q3",
    "rotation_calendar": [
        {"slot_n": 1, "scheduled_date": "2026-07-07", "cluster_id": "a", "status": "scheduled"},
        {"slot_n": 2, "scheduled_date": "2026-07-21", "cluster_id": "b", "status": "scheduled"},
        {"slot_n": 3, "scheduled_date": "2026-08-04", "cluster_id": "c", "status": "scheduled"},
    ],
    "audit_log": [{
        "slot_n": 1, "cluster_id": "a", "started_at": "2026-07-07T09:00:00Z",
        "duration_minutes": 58, "fixes_shipped": 4, "fixes_deferred": 1,
    }],
    "deferred_fixes": [{
        "fix_id": "DF-001", "logged_at": "2026-07-07", "due_date": "2026-08-06",
        "cluster_id": "a", "status": "open",
    }],
    "retrospective": {},
}
BAD = {
    "quarter": "Q3",
    "rotation_calendar": [],
    "audit_log": [{"slot_n": 1, "duration_minutes": 180}],
    "deferred_fixes": [{"fix_id": "DF", "logged_at": "2026-01-01", "due_date": "2026-04-01",
                        "cluster_id": "x", "status": "open"}],
    "retrospective": {},
}


def self_test():
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write("OK fixture rejected: " + repr(errs_ok) + "\n")
        return 1
    errs_bad = validate(BAD)
    if not errs_bad:
        sys.stderr.write("BAD fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
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
        sys.stderr.write("not a file: " + str(p) + "\n")
        return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write("VIOLATION: " + e + "\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
