#!/usr/bin/env python3
"""validate-tech-radar-thoughtworks-style.py

Validate the artefact produced by the `tech-radar-thoughtworks-style` methodology against the schema
declared in content/02-output-contract.xml. Pure stdlib.

Inputs:
    --file PATH    path to artefact JSON
    --self-test    run built-in fixtures (rc=0 on valid, rc=1 on invalid)
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (schema violation)
    2 = usage error (unreadable file, bad args)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXPECTED_SLUG = "tech-radar-thoughtworks-style"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
REQUIRED = ["slug", "version", "owner", "produced_at", "evidence", "body"]


def validate(obj) -> list:
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for key in REQUIRED:
        if key not in obj:
            errs.append(f"missing required key: {key}")
    if "slug" in obj and obj["slug"] != EXPECTED_SLUG:
        errs.append("slug mismatch: expected {!r}, got {!r}".format(EXPECTED_SLUG, obj["slug"]))
    if "version" in obj and not (isinstance(obj["version"], str) and SEMVER.match(obj["version"])):
        errs.append("version must be semver (e.g. 1.0.0)")
    if "evidence" in obj:
        ev = obj["evidence"]
        if not isinstance(ev, list) or len(ev) < 1:
            errs.append("evidence must be a non-empty array")
    if "owner" in obj and not (isinstance(obj["owner"], str) and len(obj["owner"]) >= 2):
        errs.append("owner must be a non-empty string >= 2 chars")
    return errs


VALID_FIXTURE = {
    "slug": EXPECTED_SLUG,
    "version": "1.0.0",
    "owner": "tech-lead@example.com",
    "produced_at": "2026-05-22T12:00:00Z",
    "evidence": ["https://example.com/adr/0001"],
    "body": {"summary": "ok"},
}

INVALID_FIXTURE = {
    "slug": "wrong-slug",
    "version": "v1",
    "evidence": [],
}


def self_test() -> int:
    if validate(VALID_FIXTURE):
        sys.stderr.write("self-test: valid fixture rejected\n")
        return 1
    if not validate(INVALID_FIXTURE):
        sys.stderr.write("self-test: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test: OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--file", type=str, help="Path to artefact JSON")
    ap.add_argument("--self-test", action="store_true", help="Run built-in fixtures")
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
    except json.JSONDecodeError as exc:
        sys.stderr.write(f"json parse error: {exc}\n")
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
