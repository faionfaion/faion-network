#!/usr/bin/env python3
"""
preboard-gate.py — Verify preboarding readiness 5 days before a new hire's start date.

Input:  JSON object from stdin with hire record fields.
Output: JSON with status (GREEN/RED), days_left, per-check results, and blocking items.

Usage:
  echo '{"start_date": "2026-05-01", "offer_signed_at": "2026-04-10",
         "equipment_tracking": "1Z999AA10123456784",
         "okta_user": "jsmith", "email": "jsmith@company.com",
         "manager_id": "mgr_42", "buddy_id": "peer_17",
         "calendar_url": "https://cal.company.com/onboarding/jsmith",
         "welcome_sent_at": "2026-04-25"}' | python3 preboard-gate.py

Exit code: 0 if GREEN, 1 if RED.
"""

import sys
import json
import datetime as dt

CHECKS = [
    ("offer_signed",         lambda d: bool(d.get("offer_signed_at"))),
    ("equipment_shipped",    lambda d: bool(d.get("equipment_tracking"))),
    ("accounts_provisioned", lambda d: bool(d.get("okta_user")) and bool(d.get("email"))),
    ("manager_assigned",     lambda d: bool(d.get("manager_id"))),
    ("buddy_assigned",       lambda d: bool(d.get("buddy_id"))),
    ("day1_scheduled",       lambda d: bool(d.get("calendar_url"))),
    ("welcome_email_sent",   lambda d: bool(d.get("welcome_sent_at"))),
]


def gate(d: dict) -> dict:
    start = dt.date.fromisoformat(d["start_date"])
    days_left = (start - dt.date.today()).days
    rows = [{"check": name, "ok": fn(d)} for name, fn in CHECKS]
    blocking = [r["check"] for r in rows if not r["ok"]]
    return {
        "start_date": d["start_date"],
        "days_left": days_left,
        "status": "GREEN" if not blocking else "RED",
        "blocking": blocking,
        "checks": rows,
    }


if __name__ == "__main__":
    data = json.load(sys.stdin)
    result = gate(data)
    json.dump(result, sys.stdout, indent=2)
    print()
    sys.exit(0 if result["status"] == "GREEN" else 1)
