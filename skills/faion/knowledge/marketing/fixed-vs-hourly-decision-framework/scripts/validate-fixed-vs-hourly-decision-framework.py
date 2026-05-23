#!/usr/bin/env python3
"""validate-fixed-vs-hourly-decision-framework.py

Validate one fixed-vs-hourly decision record JSON against the schema.

Inputs:
    --file PATH       path to JSON
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

BANNED = re.compile(r"^(team|we|us|agency)$", re.I)
DID = re.compile(r"^fvh-[a-z0-9-]+$")
BANDS = {"low", "medium", "high"}
SHAPES = {"fixed", "hourly", "hybrid"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("decision_id", "engagement", "signals", "options_considered", "chosen", "kill_criteria", "reversal_trigger", "decider", "decided_at", "reassessment_at_25pct"):
        if k not in obj:
            errs.append(f"missing required: {k}")
    if not DID.match(obj.get("decision_id", "")):
        errs.append("decision_id must match fvh-<slug>")
    signals = obj.get("signals") or {}
    for s in ("scope_clarity", "change_rate", "client_maturity", "domain_familiarity"):
        if signals.get(s) not in BANDS:
            errs.append(f"signals.{s} must be low/medium/high")
    if obj.get("chosen") not in SHAPES:
        errs.append(f"chosen invalid: {obj.get('chosen')!r}")
    rt = obj.get("reversal_trigger", "")
    if not isinstance(rt, str) or len(rt) < 20:
        errs.append("reversal_trigger missing or <20 chars")
    decider = obj.get("decider", "")
    if not decider or len(decider) < 3 or BANNED.match(decider.strip()):
        errs.append(f"decider invalid: {decider!r}")
    kc = obj.get("kill_criteria") or {}
    if not isinstance(kc, dict) or not kc:
        errs.append("kill_criteria must be non-empty object")
    chosen = obj.get("chosen")
    if chosen in kc and not re.search(r"\d", kc[chosen]):
        errs.append(f"kill_criteria.{chosen} must contain a numeric threshold")
    return errs


OK = {
    "decision_id": "fvh-x", "engagement": {"client": "Acme", "scope_summary": "x" * 25},
    "signals": {"scope_clarity": "high", "change_rate": "low", "client_maturity": "high", "domain_familiarity": "high"},
    "options_considered": ["fixed", "hourly", "hybrid"], "chosen": "fixed",
    "kill_criteria": {"fixed": "if change >3/week reopen", "hourly": "n/a", "hybrid": "n/a"},
    "reversal_trigger": "Change >3/week sustained 2 weeks",
    "decider": "@ruslan", "decided_at": "2026-05-23", "reassessment_at_25pct": "2026-06-04",
}
BAD = {"decision_id": "fvh-x", "decider": "team", "chosen": "fixed", "kill_criteria": {"fixed": "we'll see"}}


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
