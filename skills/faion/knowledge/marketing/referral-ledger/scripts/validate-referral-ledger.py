#!/usr/bin/env python3
"""validate-referral-ledger.py — stdlib-only validator for the Referral Ledger spec artefact.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in OK / BAD fixtures
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

REQUIRED = [
    "artefact_id",
    "owner",
    "version",
    "last_reviewed",
    "inputs_used",
    "sections",
    "decision",
]
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
PLURAL_OWNERS = {"team", "we", "us", "ourselves", "everyone", "engineering"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    owner = obj.get("owner", "")
    if isinstance(owner, str) and owner.strip().lower() in PLURAL_OWNERS:
        errs.append("owner is plural pronoun / generic group; must be a named individual")
    v = obj.get("version", "")
    if isinstance(v, str) and v and not SEMVER.match(v):
        errs.append(f"version not semver: {v!r}")
    d = obj.get("last_reviewed", "")
    if isinstance(d, str) and d and not DATE.match(d):
        errs.append(f"last_reviewed not YYYY-MM-DD: {d!r}")
    iu = obj.get("inputs_used")
    if isinstance(iu, list):
        for i, item in enumerate(iu):
            if not isinstance(item, dict) or "name" not in item or "source" not in item:
                errs.append(f"inputs_used[{i}] missing name/source")
    secs = obj.get("sections")
    if isinstance(secs, list):
        if len(secs) < 2:
            errs.append("sections must have >= 2 items")
        for i, s in enumerate(secs):
            if not isinstance(s, dict) or "heading" not in s or "body" not in s:
                errs.append(f"sections[{i}] missing heading/body")
    return errs


OK_JSON = (
    '{"artefact_id": "referral-ledger-smoke-2026-05-23", '
    '"owner": "Ruslan Faion <ruslan@faion.net>", '
    '"version": "1.0.0", '
    '"last_reviewed": "2026-05-23", '
    '"inputs_used": [{"name": "smoke", "source": "tests/fixtures/smoke.md"}], '
    '"sections": [{"heading": "Context", "body": "smoke"}, {"heading": "Decision", "body": "smoke"}], '
    '"decision": "smoke-test pass"}'
)
BAD = {"owner": "team", "inputs_used": [], "sections": []}


def self_test() -> int:
    ok = json.loads(OK_JSON)
    if validate(ok):
        sys.stderr.write("self-test FAIL: OK rejected: " + repr(validate(ok)) + "\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("self-test FAIL: BAD accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="artefact JSON file to validate")
    ap.add_argument("--self-test", action="store_true", help="run built-in OK / BAD fixtures")
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
        sys.stderr.write(f"not valid JSON: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
