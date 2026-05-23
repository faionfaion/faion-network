#!/usr/bin/env python3
"""validate-founder-led-qualification-rubric.py — schema validator."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

BANNED = re.compile(r"^(team|we|us)$", re.I)
CHECKS = {"budget", "authority", "need", "timeline", "fit"}
VERDICTS = {"qualified", "disqualified", "borderline"}


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("prospect_id", "checks", "verdict", "owner", "evaluated_at"):
        if k not in obj:
            errs.append(f"missing required: {k}")
    owner = obj.get("owner", "")
    if not owner or len(owner) < 3 or BANNED.match(owner.strip()):
        errs.append(f"owner invalid: {owner!r}")
    checks = obj.get("checks") or {}
    no_count = 0
    for c in CHECKS:
        ch = checks.get(c) or {}
        if "yes" not in ch or not isinstance(ch.get("yes"), bool):
            errs.append(f"checks.{c}.yes missing or not bool")
        if not ch.get("evidence"):
            errs.append(f"checks.{c}.evidence missing (rule evidence-per-check)")
        if ch.get("yes") is False:
            no_count += 1
    v = obj.get("verdict")
    if v not in VERDICTS:
        errs.append(f"verdict invalid: {v!r}")
    if no_count >= 3 and v != "disqualified":
        errs.append(f"3+ no's but verdict != disqualified (rule three-no-auto-disqualify)")
    return errs


OK = {
    "prospect_id": "p-101",
    "checks": {
        "budget": {"yes": True, "evidence": "x"},
        "authority": {"yes": True, "evidence": "x"},
        "need": {"yes": True, "evidence": "x"},
        "timeline": {"yes": False, "evidence": "x"},
        "fit": {"yes": True, "evidence": "x"},
    },
    "verdict": "borderline", "owner": "@ruslan", "evaluated_at": "2026-05-23",
}
BAD = {"prospect_id": "p-1", "checks": {"budget": {"yes": True}}, "verdict": "looks promising"}


def self_test():
    if validate(OK):
        sys.stderr.write(f"ok rejected: {validate(OK)}\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
    sys.stdout.write("self-test OK\n"); return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str); ap.add_argument("--self-test", action="store_true")
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
