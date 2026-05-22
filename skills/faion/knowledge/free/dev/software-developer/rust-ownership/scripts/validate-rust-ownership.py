#!/usr/bin/env python3
"""validate-rust-ownership.py — schema validator for ownership decision records.

Inputs: --file PATH | --self-test | --help
Exits: 0 valid, 1 invalid, 2 usage
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KINDS = {"owned", "shared-ref", "mutable-ref", "rc", "arc", "arc-mutex"}
LIFETIME_RE = re.compile(r"^('[a-z_]+|elided)$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("function", "answers", "signature", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    a = obj.get("answers") or {}
    for k in ("keeps_value", "modifies_value", "shares_across_threads"):
        if k not in a:
            errs.append(f"answers.{k} missing")
        elif not isinstance(a[k], bool):
            errs.append(f"answers.{k} must be boolean")
    s = obj.get("signature") or {}
    if s.get("param_kind") not in KINDS:
        errs.append(f"signature.param_kind must be in {sorted(KINDS)}")
    if "lifetime" in s and not LIFETIME_RE.match(str(s["lifetime"])):
        errs.append("signature.lifetime must be ' lowercase or 'elided'")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


OK = {
    "function": "src::s::load",
    "answers": {"keeps_value": False, "modifies_value": False, "shares_across_threads": False},
    "signature": {"param_kind": "shared-ref", "lifetime": "elided"},
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {"function": "x", "answers": {"keeps_value": "yes"}, "signature": {"param_kind": "rc-deep"}}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("OK rejected\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("BAD accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file")
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
    errs = validate(json.loads(p.read_text()))
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
