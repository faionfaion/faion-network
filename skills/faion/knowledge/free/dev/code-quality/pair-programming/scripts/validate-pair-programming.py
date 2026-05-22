#!/usr/bin/env python3
"""validate-pair-programming.py — validate a pair-programming output JSON against the methodology schema.

Inputs:
    --file PATH    JSON file to validate
    --self-test    run built-in valid + invalid fixtures
    --help         this message

Exit codes:
    0 = valid
    1 = invalid (violations on stderr)
    2 = usage / unreadable
"""
from __future__ import annotations

import argparse, json, re, sys
from pathlib import Path

REQUIRED = ['artefact_id', 'version', 'last_reviewed', 'topic', 'participants', 'style', 'swap_minutes']
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj):
    errs = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be YYYY-MM-DD")
    return errs


VALID_FIX = {k: "x" if k != "version" else "1.0.0" for k in REQUIRED}
if "last_reviewed" in VALID_FIX:
    VALID_FIX["last_reviewed"] = "2026-05-22"
INVALID_FIX = {}


def self_test():
    if validate(VALID_FIX):
        sys.stderr.write("valid fixture rejected\n"); return 1
    if not validate(INVALID_FIX):
        sys.stderr.write("invalid fixture accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    obj = json.loads(p.read_text())
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
