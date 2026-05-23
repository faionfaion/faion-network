#!/usr/bin/env python3
"""Validate prompt-pr-checklist artefact.

USAGE:
    validate-prompt-pr-review-checklist.py <input.json>
    validate-prompt-pr-review-checklist.py --self-test
    validate-prompt-pr-review-checklist.py --help

EXIT CODES:
    0 valid
    1 schema violation
    2 usage / unreadable

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MODES = {"READ-DO", "DO-CONFIRM"}
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
FORBIDDEN_OWNERS = {"team", "we", "us", "engineering", ""}


def validate(s: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(s, dict):
        return ["root must be object"]
    for k in ("artefact_id", "owner", "mode", "pause_points", "version", "last_reviewed"):
        if k not in s:
            v.append(f"missing required field: {k}")
    owner = (s.get("owner") or "").strip().lower()
    if owner in FORBIDDEN_OWNERS:
        v.append(f"owner forbidden value {owner!r}")
    if s.get("mode") not in MODES:
        v.append(f"mode must be one of {sorted(MODES)} (rule r4)")
    pps = s.get("pause_points")
    if not isinstance(pps, list) or len(pps) < 1:
        v.append("pause_points must be non-empty list")
    if isinstance(pps, list):
        for i, pp in enumerate(pps):
            if not isinstance(pp, dict):
                v.append(f"pause_points[{i}] must be object")
                continue
            items = pp.get("items")
            if not isinstance(items, list):
                v.append(f"pause_points[{i}].items must be list")
                continue
            if not (5 <= len(items) <= 9):
                v.append(f"pause_points[{i}].items length {len(items)} not in [5,9] (rule r2)")
            for j, it in enumerate(items):
                if not isinstance(it, dict):
                    v.append(f"pause_points[{i}].items[{j}] must be object")
                    continue
                for k in ("id", "statement", "executor", "artefact", "killer_anchor"):
                    if not (it.get(k) or "").strip():
                        v.append(f"pause_points[{i}].items[{j}].{k} required (rules r1,r3)")
    if not SEMVER_RE.match(s.get("version", "") or ""):
        v.append("version must be semver")
    if not DATE_RE.match(s.get("last_reviewed", "") or ""):
        v.append("last_reviewed must be ISO YYYY-MM-DD")
    return v


GOOD = {
    "artefact_id": "prompt-pr-checklist-2026q2",
    "owner": "ruslan@faion.net",
    "mode": "READ-DO",
    "pause_points": [{
        "name": "pre-merge",
        "items": [
            {"id": f"i{n}", "statement": f"item {n}", "executor": "author", "artefact": "x", "killer_anchor": f"incident-{n}"}
            for n in range(1, 6)
        ],
    }],
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "artefact_id": "x",
    "owner": "team",
    "pause_points": [{"name": "merge", "items": [{"id": "i1", "statement": "looks good"}]}],
    "version": "v1",
    "last_reviewed": "2025-01-01",
}


def _self_test() -> int:
    errs = validate(GOOD)
    assert errs == [], f"happy failed: {errs}"
    bad = validate(BAD)
    assert any("mode" in x for x in bad)
    assert any("items length" in x for x in bad)
    assert any("killer_anchor" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-prompt-pr-review-checklist.py")
    p.add_argument("path", nargs="?")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
