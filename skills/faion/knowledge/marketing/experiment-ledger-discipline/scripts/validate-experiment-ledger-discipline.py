#!/usr/bin/env python3
"""validate-experiment-ledger-discipline.py

Validate one ledger entry JSON against the schema in content/02-output-contract.xml.

Inputs:
    --file PATH       path to entry JSON
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

EID = re.compile(r"^ent-[a-z0-9-]+$")
BANNED_CONSUMER = re.compile(r"^(team|we|us)$", re.I)
STATUSES = {"proposed", "shipped", "closed", "superseded"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("entry_id", "status", "producer", "consumer", "decision_fed", "hypothesis", "tags", "cycle_id", "created_at"):
        if k not in obj:
            errs.append(f"missing required: {k}")
    if not EID.match(obj.get("entry_id", "")):
        errs.append("entry_id must match ent-<slug>")
    if obj.get("status") not in STATUSES:
        errs.append(f"status invalid: {obj.get('status')!r}")
    consumer = obj.get("consumer", "")
    if not isinstance(consumer, str) or len(consumer) < 3:
        errs.append("consumer missing")
    elif BANNED_CONSUMER.match(consumer.strip()):
        errs.append(f"consumer is plural noun: {consumer!r}")
    if not obj.get("decision_fed") or len(obj.get("decision_fed", "")) < 10:
        errs.append("decision_fed too short")
    if not obj.get("hypothesis") or len(obj.get("hypothesis", "")) < 20:
        errs.append("hypothesis too short")
    tags = obj.get("tags") or []
    if not isinstance(tags, list) or not tags:
        errs.append("tags must be non-empty array")
    if obj.get("status") == "closed":
        ls = obj.get("learning_summary") or ""
        if not isinstance(ls, str) or len(ls) < 80:
            errs.append("learning_summary < 80 chars at close (rule learning-summary-required)")
    if obj.get("status") == "superseded" and not obj.get("superseded_by"):
        errs.append("status=superseded but superseded_by missing (rule superseded-by-chain)")
    if obj.get("prev_entry_id") and not obj.get("delta_reason"):
        errs.append("prev_entry_id without delta_reason (rule append-only)")
    return errs


OK = {
    "entry_id": "ent-x", "status": "closed", "producer": "@alex", "consumer": "@beth",
    "decision_fed": "decide pricing layout next cycle",
    "hypothesis": "Moving social proof above fold lifts conversion.",
    "tags": ["pricing"], "cycle_id": "2026-Q2", "created_at": "2026-04-15T00:00:00Z",
    "learning_summary": "x" * 100,
}
BAD = {"entry_id": "ent-x", "status": "closed", "producer": "a", "consumer": "team"}


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
