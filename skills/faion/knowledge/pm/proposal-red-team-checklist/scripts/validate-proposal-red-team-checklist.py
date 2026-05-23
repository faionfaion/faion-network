#!/usr/bin/env python3
"""validate-proposal-red-team-checklist.py

Validate a RedTeamChecklist JSON against content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH       path to checklist JSON
    --self-test       run built-in fixtures
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

MODES = {"READ-DO", "DO-CONFIRM"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("proposal_id", "header", "pause_points"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if errs:
        return errs

    h = obj["header"]
    for k in ("owner", "mode", "last_reviewed", "version"):
        if k not in h:
            errs.append(f"header.{k} missing")
    if h.get("mode") not in MODES:
        errs.append(f"header.mode invalid (rule: r1-read-do-discipline)")
    owner = h.get("owner", {})
    if not owner.get("person"):
        errs.append("header.owner.person empty (rule: r4-named-execution / fm-02)")
    if owner.get("role") in {"team", "channel", ""}:
        errs.append("header.owner.role too vague")
    lr = h.get("last_reviewed", "")
    try:
        d = dt.date.fromisoformat(lr)
        if (dt.date.today() - d).days > 90:
            errs.append(f"header.last_reviewed {lr} > 90 days (rule: r5-review-cadence)")
    except Exception:
        errs.append("header.last_reviewed not ISO date")

    pps = obj["pause_points"]
    if not isinstance(pps, list) or not pps:
        errs.append("pause_points must be non-empty list")
        return errs
    for i, pp in enumerate(pps):
        items = pp.get("items", [])
        if not (5 <= len(items) <= 9):
            errs.append(f"pause_points[{i}] '{pp.get('name')}': {len(items)} items, must be 5-9 (rule: r2-bounded-length)")
        for j, it in enumerate(items):
            for f in ("item_id", "text", "executor", "artefact", "killer_anchor"):
                if not it.get(f):
                    errs.append(f"pause_points[{i}].items[{j}].{f} empty (rule: r4-named-execution / r3-killer-items-only)")
            if len(it.get("text", "")) < 10:
                errs.append(f"pause_points[{i}].items[{j}].text too short")
    return errs


SMOKE_OK_FILE = Path(__file__).parent.parent / "templates" / "_smoke-test.json"
SMOKE_BAD = {
    "proposal_id": "x",
    "header": {"owner": {"role": "team", "person": ""}, "mode": "FREESTYLE",
               "last_reviewed": "2025-08-01", "version": "1.0"},
    "pause_points": [{"name": "Scope", "items": [
        {"item_id": "S1", "text": "ok", "executor": "", "artefact": "", "killer_anchor": ""}
    ]}]
}


def self_test() -> int:
    if SMOKE_OK_FILE.is_file():
        ok = json.loads(SMOKE_OK_FILE.read_text())
        # Re-stamp last_reviewed to today so test does not bit-rot
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
