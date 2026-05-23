#!/usr/bin/env python3
"""validate-ih-build-update-template.py

Validate an IH build-update post bundle against content/02-output-contract.xml.

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
from pathlib import Path

VAGUE_ASK = re.compile(r"\b(thoughts\?|any feedback\?|what do you think\?)\b", re.I)
WEEKDAYS = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("title", "tldr", "body", "numbers", "ask", "scheduled_at"):
        if k not in obj:
            errs.append("missing " + k)
    title = obj.get("title", "")
    if not isinstance(title, str) or not (10 <= len(title) <= 100):
        errs.append("title length must be [10,100]")
    tldr = obj.get("tldr", "")
    if not isinstance(tldr, str) or not (20 <= len(tldr) <= 180):
        errs.append("tldr length must be [20,180]")
    if isinstance(tldr, str) and not tldr.startswith("TL;DR:"):
        errs.append("tldr must start with 'TL;DR:'")
    body = obj.get("body", "")
    if not isinstance(body, str) or not (600 <= len(body) <= 1200):
        errs.append("body length must be [600,1200]")
    nums = obj.get("numbers", [])
    if not isinstance(nums, list) or len(nums) != 3:
        errs.append("numbers must be array of length 3")
    else:
        for i, n in enumerate(nums):
            for k in ("label", "value", "window_days"):
                if k not in n:
                    errs.append("numbers[" + str(i) + "] missing " + k)
            if "window_days" in n and not (1 <= n["window_days"] <= 30):
                errs.append("numbers[" + str(i) + "] window_days must be [1,30]")
    ask = obj.get("ask", "")
    if not isinstance(ask, str) or not (15 <= len(ask) <= 220):
        errs.append("ask length must be [15,220]")
    if isinstance(ask, str) and VAGUE_ASK.search(ask.strip()):
        errs.append("ask matches vague-ask pattern")
    wd = obj.get("weekday_et")
    if wd is not None and wd not in WEEKDAYS:
        errs.append("weekday_et not in enum")
    if wd is not None and wd != "tue":
        errs.append("weekday_et must be 'tue' for IH algorithm slot")
    hr = obj.get("hour_et")
    if hr is not None and hr not in (8, 9, 10):
        errs.append("hour_et must be 8, 9, or 10 ET")
    return errs


OK = {
    "title": "Week 14 — first $1k MRR, here is what flipped it",
    "tldr": "TL;DR: hit $1k MRR week 14 after switching to one-niche DMs. Two questions for IH on what to test next.",
    "body": "x" * 800,
    "numbers": [
        {"label": "MRR", "value": "$1040", "window_days": 7},
        {"label": "Trial-to-paid", "value": "21%", "window_days": 7},
        {"label": "DMs sent", "value": "47", "window_days": 7},
    ],
    "ask": "If you hit $1k MRR via cold outreach, what opener worked — verbatim if possible?",
    "scheduled_at": "2026-05-26T13:00:00Z",
    "weekday_et": "tue",
    "hour_et": 9,
}
BAD = {
    "title": "x",
    "tldr": "thoughts about progress",
    "body": "short",
    "numbers": [],
    "ask": "thoughts?",
    "scheduled_at": "2026-05-25T09:00:00Z",
    "weekday_et": "sun",
    "hour_et": 22,
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
