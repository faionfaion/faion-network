#!/usr/bin/env python3
"""validate-web-scraping-resilience.py

Validate a resilience config JSON against the schema + rule consistency.

Inputs:
    --file PATH      path to config JSON
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

ID_RE = re.compile(r"^wsrr-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    required = [
        "artefact_id", "source",
        "delay_ms_min", "delay_ms_max",
        "max_retries", "base_delay_ms",
        "safe_extract_timeout_ms",
        "anti_detect_enabled", "crash_recover_enabled",
        "concurrency_cap", "version", "last_reviewed",
    ]
    for k in required:
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^wsrr-[a-z0-9-]{6,}$")

    dmin = obj.get("delay_ms_min")
    dmax = obj.get("delay_ms_max")
    for k, v in (("delay_ms_min", dmin), ("delay_ms_max", dmax)):
        if not isinstance(v, int) or not (100 <= v <= 60000):
            errs.append(f"{k} must be int in [100, 60000]")
    if isinstance(dmin, int) and isinstance(dmax, int):
        if dmin > dmax:
            errs.append("delay_ms_min must be <= delay_ms_max")
        if dmin == dmax:
            errs.append("delay_ms_min == delay_ms_max — no jitter (r1 violation)")

    mr = obj.get("max_retries")
    if not isinstance(mr, int) or not (0 <= mr <= 5):
        errs.append("max_retries must be int in [0,5]")

    bd = obj.get("base_delay_ms")
    if not isinstance(bd, int) or not (100 <= bd <= 10000):
        errs.append("base_delay_ms must be int in [100, 10000]")

    se = obj.get("safe_extract_timeout_ms")
    if not isinstance(se, int) or not (100 <= se <= 5000):
        errs.append("safe_extract_timeout_ms must be int in [100, 5000]")

    for k in ("anti_detect_enabled", "crash_recover_enabled"):
        if not isinstance(obj.get(k), bool):
            errs.append(f"{k} must be boolean")

    cap = obj.get("concurrency_cap")
    if not isinstance(cap, int) or not (1 <= cap <= 50):
        errs.append("concurrency_cap must be int in [1, 50]")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "wsrr-news-2026-05",
    "source": "example.com/news",
    "delay_ms_min": 1000,
    "delay_ms_max": 3000,
    "max_retries": 5,
    "base_delay_ms": 500,
    "safe_extract_timeout_ms": 5000,
    "anti_detect_enabled": True,
    "crash_recover_enabled": True,
    "concurrency_cap": 3,
    "stealth_lib": "playwright-stealth",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "news",
    "source": "example.com/news",
    "delay_ms_min": 50,
    "delay_ms_max": 50,
    "max_retries": 100,
    "base_delay_ms": 50,
    "safe_extract_timeout_ms": 30000,
    "anti_detect_enabled": False,
    "crash_recover_enabled": False,
    "concurrency_cap": 100,
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
    ap.add_argument("--file", type=str, help="path to resilience config JSON")
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
