#!/usr/bin/env python3
"""validate-small-team-comms-rhythm.py

Validate a CommsRhythmConfig JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to config JSON
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

RITUAL_IDS = {"daily_pulse", "weekly_sync", "monthly_direction"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("team_id", "header", "team_size", "rituals", "cycle_log"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs
    h = obj["header"]
    if not h.get("owner", {}).get("person"):
        errs.append("header.owner.person empty")
    lr = h.get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
        if (dt.date.today() - d).days > 90:
            errs.append(f"header.last_reviewed {lr} > 90 days")
    except Exception:
        errs.append("header.last_reviewed not ISO date")

    ts = obj["team_size"]
    if not isinstance(ts, int) or not (2 <= ts <= 3):
        errs.append(f"team_size {ts} not in [2,3] (rule: r5-graduation-trigger)")

    if len(obj["rituals"]) != 3:
        errs.append(f"rituals length {len(obj['rituals'])} != 3 (rule: r1-three-rituals-only)")
    ritual_ids_seen = set()
    for i, r in enumerate(obj["rituals"]):
        rid = r.get("ritual_id")
        if rid not in RITUAL_IDS:
            errs.append(f"rituals[{i}].ritual_id invalid (rule: r1-three-rituals-only)")
        ritual_ids_seen.add(rid)
        if rid == "daily_pulse" and r.get("mode") != "async":
            errs.append(f"rituals[{i}] daily_pulse mode must be async (rule: r3-async-by-default)")
        if rid == "weekly_sync" and r.get("duration_minutes_cap", 0) > 30:
            errs.append(f"rituals[{i}] weekly_sync > 30 min (rule: r4-weekly-30-min-cap)")

    if ritual_ids_seen != RITUAL_IDS:
        errs.append(f"rituals must cover exactly {RITUAL_IDS}")

    for i, c in enumerate(obj["cycle_log"]):
        if c.get("founder_only") is True:
            errs.append(f"cycle_log[{i}] founder_only=true (rule: r2-founder-not-presenter)")
        if c.get("ritual_id") == "weekly_sync" and c.get("agenda_published_24h") is False:
            errs.append(f"cycle_log[{i}] weekly_sync without 24h agenda (rule: r4-weekly-30-min-cap)")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "team_id": "x",
    "header": {"owner": {"role": "team", "person": ""}, "last_reviewed": "2024-01-01", "version": "0"},
    "team_size": 5,
    "rituals": [
        {"ritual_id": "daily_pulse", "name": "Daily standup zoom", "mode": "sync", "duration_minutes_cap": 15},
        {"ritual_id": "weekly_sync", "name": "Weekly", "mode": "sync", "duration_minutes_cap": 60},
        {"ritual_id": "monthly_direction", "name": "Monthly", "mode": "sync", "duration_minutes_cap": 45}
    ],
    "cycle_log": [{"cycle_iso": "2026-W20", "ritual_id": "weekly_sync", "founder_only": True, "agenda_published_24h": False}]
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
