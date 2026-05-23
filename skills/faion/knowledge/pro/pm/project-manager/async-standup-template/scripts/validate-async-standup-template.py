#!/usr/bin/env python3
"""validate-async-standup-template.py

Validate a daily-standup post or weekly-digest JSON against the schema declared
in content/02-output-contract.xml. Stdlib-only.

Inputs:
    --file PATH    path to post or digest JSON
    --self-test    run built-in fixtures and exit
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

WINDOW_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\.\.[0-9]{4}-[0-9]{2}-[0-9]{2}$")
BANNED_PLACEHOLDERS = ("TBD", "WIP", "TODO", "FIXME")


def validate_post(o: dict) -> list[str]:
    errs: list[str] = []
    for k in ("kind", "author", "posted_at", "yesterday", "today", "blocker"):
        if k not in o:
            errs.append(f"post.{k} missing")
    if errs:
        return errs
    if not isinstance(o["yesterday"], str) or not (1 <= len(o["yesterday"]) <= 400):
        errs.append("post.yesterday length invalid")
    if not isinstance(o["today"], str) or not (1 <= len(o["today"]) <= 400):
        errs.append("post.today length invalid")
    for k in ("yesterday", "today", "blocker"):
        for ph in BANNED_PLACEHOLDERS:
            if isinstance(o.get(k), str) and ph in o[k]:
                errs.append(f"post.{k} contains banned placeholder {ph!r}")
    blocker = o.get("blocker", "")
    if isinstance(blocker, str) and blocker.strip().lower() not in ("none", ""):
        if not o.get("blocker_owner"):
            errs.append("post.blocker non-'none' without blocker_owner")
    if o.get("yesterday") and o.get("today") and o["yesterday"].strip() == o["today"].strip():
        errs.append("post.yesterday == post.today (copy-paste signal)")
    total_words = sum(len(o.get(k, "").split()) for k in ("yesterday", "today", "blocker"))
    if total_words > 250:
        errs.append(f"post total words {total_words} > 250")
    return errs


def validate_digest(o: dict) -> list[str]:
    errs: list[str] = []
    for k in ("kind", "author", "week_window", "shipped", "in_progress",
              "unresolved_blockers", "missed_posters", "next_week_risk"):
        if k not in o:
            errs.append(f"digest.{k} missing")
    if errs:
        return errs
    if not WINDOW_RE.match(str(o["week_window"])):
        errs.append(f"digest.week_window pattern invalid: {o['week_window']!r}")
    for k in ("shipped", "in_progress"):
        v = o[k]
        if not isinstance(v, list) or len(v) > 7:
            errs.append(f"digest.{k} must be list, max 7 items")
    if not isinstance(o.get("next_week_risk"), str) or len(o["next_week_risk"]) > 400:
        errs.append("digest.next_week_risk must be ≤400 char string")
    return errs


def validate(obj: dict) -> list[str]:
    if not isinstance(obj, dict):
        return ["root must be object"]
    kind = obj.get("kind")
    if kind == "post":
        return validate_post(obj)
    if kind == "digest":
        return validate_digest(obj)
    return [f"unknown kind: {kind!r} (expected 'post' or 'digest')"]


GOOD_POST = {
    "kind": "post", "author": "U", "posted_at": "2026-05-23T08:15:00+02:00",
    "yesterday": "Shipped checkout v2.", "today": "Roll out canary.",
    "blocker": "Need DB window", "blocker_owner": "U_RAJ",
}
BAD_POST = {
    "kind": "post", "author": "U", "posted_at": "2026-05-23T08:15:00+02:00",
    "yesterday": "Same.", "today": "Same.",
    "blocker": "Need migration", "blocker_owner": None,
}


def self_test() -> int:
    if validate(GOOD_POST):
        sys.stderr.write("good post rejected\n"); return 1
    if not validate(BAD_POST):
        sys.stderr.write("bad post accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n"); return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
