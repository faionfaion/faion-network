#!/usr/bin/env python3
"""validate-role-cheatsheet-generator.py — validate generated cheatsheet artefact.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixture (valid + invalid)
    --help            show this message

Exit codes:
    0 = valid OR self-test passed
    1 = invalid OR self-test failed
    2 = usage / unreadable input
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = ["corpus_version", "role", "tier", "top_n", "entries", "overrides_merged"]
TIER_ORDER = ["free", "solo", "pro", "geek"]

VALID_FIXTURE = {
    "corpus_version": "2026-05-23",
    "role": "software-architect",
    "tier": "pro",
    "top_n": 2,
    "entries": [
        {"rank": 1, "slug": "pro/infra/greenfield-infra-decision-matrix", "tier": "pro", "priority_signal": 42.0},
        {"rank": 2, "slug": "pro/infra/capacity-planning-at-design-time", "tier": "pro", "priority_signal": 38.0},
    ],
    "overrides_merged": 2,
}

INVALID_FIXTURE = {
    "corpus_version": "2026-05-23",
    "role": "software-architect",
    "tier": "pro",
    "top_n": 30,
    "entries": [{"rank": 1, "slug": "geek/ai/foo", "tier": "geek", "priority_signal": 99}],
    "overrides_merged": 0,
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    tn = obj.get("top_n")
    if not isinstance(tn, int) or not (1 <= tn <= 10):
        errs.append("top_n: must be integer 1..10")
    org_tier = obj.get("tier")
    if org_tier not in TIER_ORDER:
        errs.append(f"tier: not in {TIER_ORDER}")
    org_idx = TIER_ORDER.index(org_tier) if org_tier in TIER_ORDER else -1
    entries = obj.get("entries", [])
    if not isinstance(entries, list) or not (1 <= len(entries) <= 10):
        errs.append("entries: must be array 1..10")
    else:
        for i, e in enumerate(entries):
            et = e.get("tier")
            if et not in TIER_ORDER:
                errs.append(f"entries[{i}].tier: not in {TIER_ORDER}")
            elif org_idx >= 0 and TIER_ORDER.index(et) > org_idx:
                errs.append(f"entries[{i}].tier: {et!r} above org tier {org_tier!r} (tier-gate breach)")
    om = obj.get("overrides_merged")
    if not isinstance(om, int) or not (0 <= om <= 5):
        errs.append("overrides_merged: must be integer 0..5")
    return errs


def self_test() -> int:
    errs_ok = validate(VALID_FIXTURE)
    if errs_ok:
        sys.stderr.write("self-test: VALID fixture rejected:\n  " + "\n  ".join(errs_ok) + "\n")
        return 1
    errs_bad = validate(INVALID_FIXTURE)
    if not errs_bad:
        sys.stderr.write("self-test: INVALID fixture accepted (should fail)\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except Exception as e:
        sys.stderr.write(f"unreadable JSON: {e}\n")
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
