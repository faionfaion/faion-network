#!/usr/bin/env python3
"""validate-rust-testing.py — schema validator for Rust test-strategy spec."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("layers", "coverage", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    layers = obj.get("layers") or {}
    for k in ("unit", "integration", "doctest"):
        if layers.get(k) is not True:
            errs.append(f"layers.{k} must be true")
    cov = obj.get("coverage") or {}
    if cov.get("tool") != "cargo-llvm-cov":
        errs.append("coverage.tool must be 'cargo-llvm-cov'")
    dt = cov.get("diff_threshold")
    if not isinstance(dt, int) or not (80 <= dt <= 95):
        errs.append("coverage.diff_threshold must be int in [80,95]")
    if "proptest_cases" in obj:
        n = obj["proptest_cases"]
        if not isinstance(n, int) or not (64 <= n <= 65536):
            errs.append("proptest_cases must be int in [64,65536]")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


OK = {
    "layers": {"unit": True, "integration": True, "doctest": True, "proptest": True},
    "coverage": {"tool": "cargo-llvm-cov", "diff_threshold": 85},
    "proptest_cases": 1024,
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {
    "layers": {"unit": True, "integration": False, "doctest": False},
    "coverage": {"tool": "tarpaulin", "diff_threshold": 60},
}


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
