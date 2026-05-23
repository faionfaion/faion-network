#!/usr/bin/env python3
"""validate-guardrails-nemo.py — validate config.yml shape.

Inputs:
    --file PATH    YAML or JSON file
    --self-test
    --help

Exit codes: 0 valid; 1 invalid; 2 usage.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

REQUIRED = ["artefact_id", "version", "last_reviewed", "models", "rails"]
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be YYYY-MM-DD")
    ms = obj.get("models", [])
    if not isinstance(ms, list) or not ms:
        errs.append("models must be non-empty list")
    rails = obj.get("rails", {})
    if not isinstance(rails, dict):
        errs.append("rails must be object")
    else:
        for stage in ("input", "output"):
            s = rails.get(stage, {})
            if not isinstance(s, dict) or "flows" not in s:
                errs.append(f"rails.{stage}.flows missing")
    return errs


VALID_FIX = {
    "artefact_id": "x", "version": "1.0.0", "last_reviewed": "2026-05-22",
    "models": [{"type": "main", "engine": "openai", "model": "gpt-4o"}],
    "rails": {"input": {"flows": ["self check input"]}, "output": {"flows": ["self check output"]}},
}
INVALID_FIX: dict = {}


def self_test() -> int:
    if validate(VALID_FIX):
        sys.stderr.write("valid rejected\n"); return 1
    if not validate(INVALID_FIX):
        sys.stderr.write("invalid accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def load(p: Path) -> object:
    raw = p.read_text()
    if p.suffix in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("pyyaml required for yaml input")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
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
    errs = validate(load(p))
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
