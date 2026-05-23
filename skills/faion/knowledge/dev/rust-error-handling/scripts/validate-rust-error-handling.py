#!/usr/bin/env python3
"""validate-rust-error-handling.py — schema validator for error-design spec.

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
CRATE_TYPES = {"library", "binary", "build-script"}
LIBS = {"thiserror", "anyhow", "box-dyn-error"}
VARIANT_NAME_RE = re.compile(r"^[A-Z][A-Za-z0-9]+$")


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("crate_type", "error_library", "clippy_gate", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("crate_type") and obj["crate_type"] not in CRATE_TYPES:
        errs.append(f"crate_type must be in {sorted(CRATE_TYPES)}")
    if obj.get("error_library") and obj["error_library"] not in LIBS:
        errs.append(f"error_library must be in {sorted(LIBS)}")
    if obj.get("crate_type") == "library" and obj.get("error_library") != "thiserror":
        errs.append("library crates must use thiserror")
    cg = obj.get("clippy_gate") or {}
    if cg.get("unwrap_used") != "deny":
        errs.append("clippy_gate.unwrap_used must be 'deny'")
    if cg.get("expect_used") != "deny":
        errs.append("clippy_gate.expect_used must be 'deny'")
    variants = obj.get("variants", [])
    if not isinstance(variants, list):
        errs.append("variants must be list")
    else:
        for i, v in enumerate(variants):
            if not isinstance(v, dict) or "name" not in v or "display" not in v:
                errs.append(f"variants[{i}] needs name + display")
                continue
            if not VARIANT_NAME_RE.match(v["name"]):
                errs.append(f"variants[{i}].name must be PascalCase")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


OK = {
    "crate_type": "library",
    "error_library": "thiserror",
    "variants": [{"name": "Io", "display": "I/O", "from": "std::io::Error"}],
    "clippy_gate": {"unwrap_used": "deny", "expect_used": "deny"},
    "version": "1.0.0",
    "last_reviewed": "2026-05-22",
}
BAD = {"crate_type": "library", "error_library": "anyhow", "clippy_gate": {"unwrap_used": "warn"}}


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
