#!/usr/bin/env python3
"""validate-design-critique.py

Validate a Design Critique artefact against the JSON Schema (draft-07) defined in
`content/02-output-contract.xml`. Stdlib-only; no external pip deps.

Inputs:
    --file PATH       path to artefact JSON
    --self-test       run built-in fixtures (OK / BAD)
    --help            this message

Exit codes:
    0 = valid
    1 = invalid (violations printed to stderr)
    2 = usage / unreadable / parse error
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

FORBIDDEN_OWNERS = {"team", "we", "us", "ourselves", "everyone", "engineering", "tbd", "n/a", ""}

SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be an object"]
    for k in REQUIRED:
        if k not in obj or obj[k] in (None, "", []):
            errs.append(f"missing or empty required field: {k}")
    owner = obj.get("owner", "")
    if isinstance(owner, str) and owner.strip().lower() in FORBIDDEN_OWNERS:
        errs.append(f"owner is a plural pronoun / generic group: {owner!r}")
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
    sec = obj.get("sections")
    if isinstance(sec, list):
        if len(sec) < 2:
            errs.append("sections must have ≥2 entries")
        for i, item in enumerate(sec):
            if not isinstance(item, dict) or "heading" not in item or "body" not in item:
                errs.append(f"sections[{i}] missing heading/body")
    return errs


OK = {
    "artefact_id": "design-critique-2026-05-23",
    "owner": "Ruslan Faion <ruslan@faion.net>",
    "version": "1.1.0",
    "last_reviewed": "2026-05-23",
    "inputs_used": [{"name": "engagement-charter", "source": "docs/charter.md"}],
    "sections": [
        {"heading": "Context", "body": "bounded scope"},
        {"heading": "Decision", "body": "adopt"},
    ],
    "decision": "Adopt the methodology",
}

BAD = {"owner": "team", "inputs_used": []}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write(f"self-test FAIL: OK rejected: {validate(OK)!r}\n")
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
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parse error: {e}\n")
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
