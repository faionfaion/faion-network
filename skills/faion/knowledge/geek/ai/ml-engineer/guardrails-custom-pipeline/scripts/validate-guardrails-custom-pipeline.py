#!/usr/bin/env python3
"""validate-guardrails-custom-pipeline.py — validate GuardrailResult JSON against the methodology schema.

Inputs:
    --file PATH    JSON file to validate
    --self-test    run built-in fixtures
    --help         this message

Exit codes:
    0 = valid; 1 = invalid (violations on stderr); 2 = usage / unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = [
    "artefact_id", "version", "last_reviewed",
    "is_safe", "input_modified", "output_modified",
    "violations", "metadata",
]
V_TYPES = {"length", "pii", "injection", "moderation", "hallucination"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    for k in ("is_safe", "input_modified", "output_modified"):
        if k in obj and not isinstance(obj[k], bool):
            errs.append(f"{k} must be boolean")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be YYYY-MM-DD")
    vs = obj.get("violations", [])
    if not isinstance(vs, list):
        errs.append("violations must be list")
    else:
        for i, v in enumerate(vs):
            if not isinstance(v, dict) or v.get("type") not in V_TYPES:
                errs.append(f"violations[{i}].type invalid")
            if "detail" not in v:
                errs.append(f"violations[{i}].detail missing")
    md = obj.get("metadata")
    if not isinstance(md, dict) or "model" not in md:
        errs.append("metadata.model missing")
    return errs


VALID_FIX = {
    "artefact_id": "x", "version": "1.0.0", "last_reviewed": "2026-05-22",
    "is_safe": True, "input_modified": False, "output_modified": False,
    "violations": [], "metadata": {"model": "gpt-4o"},
}
INVALID_FIX: dict = {}


def self_test() -> int:
    if validate(VALID_FIX):
        sys.stderr.write("valid rejected\n"); return 1
    if not validate(INVALID_FIX):
        sys.stderr.write("invalid accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


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
    errs = validate(json.loads(p.read_text()))
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
