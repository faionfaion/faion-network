#!/usr/bin/env python3
"""validate-web-scraping-pagination.py

Validate a pagination walk-report JSON against the schema + rule consistency.

Inputs:
    --file PATH      path to walk-report JSON
    --self-test      run built-in valid + invalid fixtures
    --help           this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PATTERNS = {"next-button", "infinite-scroll", "load-more"}
VERDICTS = {"approve", "block-wrong-pattern", "block-no-dedupe", "block-unbounded-concurrency"}
ID_RE = re.compile(r"^wsp-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOFT_CAP = 10
HARD_CAP = 50


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "source", "pattern", "pages_walked", "items_collected", "duplicate_count", "concurrency_cap", "pool_high_water_mark", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^wsp-[a-z0-9-]{6,}$")

    p = obj.get("pattern")
    if p not in PATTERNS:
        errs.append(f"pattern must be one of {sorted(PATTERNS)}")

    pw = obj.get("pages_walked")
    if not isinstance(pw, int) or pw < 1:
        errs.append("pages_walked must be int >= 1")

    items = obj.get("items_collected", 0)
    dup = obj.get("duplicate_count", 0)
    if not isinstance(items, int) or items < 0:
        errs.append("items_collected must be non-negative integer")
    if not isinstance(dup, int) or dup < 0:
        errs.append("duplicate_count must be non-negative integer")

    cap = obj.get("concurrency_cap")
    hwm = obj.get("pool_high_water_mark")
    if not isinstance(cap, int) or not (1 <= cap <= HARD_CAP):
        errs.append(f"concurrency_cap must be int in [1,{HARD_CAP}]")
    if not isinstance(hwm, int) or hwm < 0:
        errs.append("pool_high_water_mark must be non-negative integer")
    if isinstance(cap, int) and isinstance(hwm, int) and hwm > cap:
        errs.append("pool_high_water_mark > concurrency_cap — leak detected")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")

    if verdict == "approve":
        if isinstance(cap, int) and cap > SOFT_CAP:
            errs.append(f"verdict=approve with concurrency_cap > {SOFT_CAP} requires explicit justification (not present)")
        if p in {"infinite-scroll", "load-more"} and isinstance(items, int) and items > 50 and dup == 0:
            errs.append("verdict=approve forbidden when pattern requires overlap-dedupe and duplicate_count=0 with >50 items")
        if isinstance(cap, int) and isinstance(hwm, int) and hwm > cap:
            errs.append("verdict=approve forbidden when pool_high_water_mark > concurrency_cap")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "wsp-news-walk-2026-05-23",
    "source": "example.com/news",
    "pattern": "infinite-scroll",
    "pages_walked": 12,
    "items_collected": 240,
    "duplicate_count": 18,
    "concurrency_cap": 3,
    "pool_high_water_mark": 3,
    "stop_condition_observed": "scrollHeight stable for 4s",
    "verdict": "approve",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "walk",
    "source": "example.com/news",
    "pattern": "next-button",
    "pages_walked": 1000,
    "items_collected": 20000,
    "duplicate_count": 0,
    "concurrency_cap": 100,
    "pool_high_water_mark": 87,
    "verdict": "approve",
    "version": "1.0",
    "last_reviewed": "today",
}


def self_test() -> int:
    errs = validate(VALID_FIXTURE)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid fixture rejected: {errs}\n")
        return 1
    errs = validate(INVALID_FIXTURE)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to walk-report JSON")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
