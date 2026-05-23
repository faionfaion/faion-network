#!/usr/bin/env python3
"""validate-hook-bank-template.py

Validate a hook-bank artefact (JSON shape) against content/02-output-contract.xml.

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

ALLOWED_PLATFORMS = {"x", "linkedin", "indiehackers", "threads"}
ALLOWED_BUCKETS = {"flopped", "average", "spiked"}
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
PATTERN_RE = re.compile(r"^[a-z][a-z-]*$")


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in ("version", "platform_medians", "rows", "patterns_active", "reviewed_at"):
        if k not in obj:
            errs.append("missing required field: " + k)
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    medians = obj.get("platform_medians", {})
    if not isinstance(medians, dict) or not medians:
        errs.append("platform_medians must be non-empty object")
    else:
        for plat, val in medians.items():
            if not isinstance(val, int) or val < 1:
                errs.append("platform_medians[" + plat + "] must be int >= 1")
    patterns = obj.get("patterns_active", [])
    if not isinstance(patterns, list) or not patterns:
        errs.append("patterns_active must be non-empty list")
    elif len(patterns) > 15:
        errs.append("patterns_active exceeds cap of 15")
    rows = obj.get("rows", [])
    if not isinstance(rows, list) or not rows:
        errs.append("rows must be non-empty list")
    else:
        for i, row in enumerate(rows):
            for k in ("hook_text", "pattern", "platform", "post_url",
                      "impressions_24h", "qualified_replies", "bucket"):
                if k not in row:
                    errs.append("rows[" + str(i) + "] missing " + k)
            if "platform" in row and row["platform"] not in ALLOWED_PLATFORMS:
                errs.append("rows[" + str(i) + "] platform not in enum")
            if "bucket" in row and row["bucket"] not in ALLOWED_BUCKETS:
                errs.append("rows[" + str(i) + "] bucket not in enum")
            if "hook_text" in row and (not isinstance(row["hook_text"], str)
                                       or len(row["hook_text"]) < 5):
                errs.append("rows[" + str(i) + "] hook_text too short")
            # bucket math check
            if all(k in row for k in ("impressions_24h", "platform", "bucket")):
                plat = row["platform"]
                med = medians.get(plat) if isinstance(medians, dict) else None
                if isinstance(med, int) and med > 0 and isinstance(row["impressions_24h"], int):
                    ratio = row["impressions_24h"] / med
                    expected = "flopped" if ratio <= 0.5 else ("spiked" if ratio >= 2.0 else "average")
                    if expected != row["bucket"]:
                        errs.append("rows[" + str(i) + "] bucket=" + row["bucket"]
                                    + " disagrees with ratio " + ("%.2f" % ratio))
    return errs


OK = {
    "version": "1.1.0",
    "platform_medians": {"x": 1400},
    "patterns_active": ["before-after", "mistake-confession"],
    "rows": [{
        "hook_text": "Shipped a $0 invoice to 312 customers last night. Postmortem.",
        "pattern": "mistake-confession",
        "platform": "x",
        "post_url": "https://x.com/u/status/1",
        "impressions_24h": 11400,
        "qualified_replies": 38,
        "bucket": "spiked",
        "flop_streak": 0,
    }],
    "reviewed_at": "2026-05-23",
}
BAD = {
    "version": "1",
    "platform_medians": {},
    "patterns_active": [],
    "rows": [{"hook_text": "x", "platform": "tiktok"}],
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
