#!/usr/bin/env python3
"""validate-qa-ai-generated-test-audit-checklist.py — validate the filled checklist.

Inputs:
    --file PATH       path to artefact JSON (filled checklist, YAML→JSON)
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

REQUIRED = ["pr_id", "reviewer", "run_at", "items", "overall_verdict"]
VERDICT_ENUM = {"pass", "flag", "n/a"}
OVERALL_ENUM = {"approve", "request_changes", "block"}

VALID_FIXTURE = {
    "pr_id": "#482",
    "reviewer": "ruslan",
    "run_at": "2026-05-23T10:00:00Z",
    "items": [{"item_id": i, "verdict": "pass"} for i in range(1, 13)],
    "overall_verdict": "approve",
}

INVALID_FIXTURE = {
    "pr_id": "#482",
    "reviewer": "ruslan",
    "run_at": "2026-05-23T10:00:00Z",
    "items": [{"item_id": 1, "verdict": "flag"}, {"item_id": 2, "verdict": "pass"}],
    "overall_verdict": "approve",
}


def validate(obj) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root: must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    items = obj.get("items", [])
    if not isinstance(items, list) or len(items) != 12:
        errs.append("items: must be array of exactly 12 entries")
    else:
        seen_ids = set()
        any_flag = False
        for i, it in enumerate(items):
            if not isinstance(it, dict):
                errs.append(f"items[{i}]: must be object")
                continue
            iid = it.get("item_id")
            if not isinstance(iid, int) or not (1 <= iid <= 12):
                errs.append(f"items[{i}].item_id: must be integer 1..12")
            elif iid in seen_ids:
                errs.append(f"items[{i}].item_id: duplicate {iid}")
            else:
                seen_ids.add(iid)
            v = it.get("verdict")
            if v not in VERDICT_ENUM:
                errs.append(f"items[{i}].verdict: {v!r} not in {sorted(VERDICT_ENUM)}")
            if v == "flag":
                any_flag = True
                if not it.get("repair_request"):
                    errs.append(f"items[{i}]: flag requires repair_request")
        ov = obj.get("overall_verdict")
        if ov == "approve" and any_flag:
            errs.append("overall_verdict: approve while items contain flag (forbidden)")
    ov = obj.get("overall_verdict")
    if ov not in OVERALL_ENUM:
        errs.append(f"overall_verdict: {ov!r} not in {sorted(OVERALL_ENUM)}")
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
