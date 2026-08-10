#!/usr/bin/env python3
"""validate-tool-description-as-prompt.py

Validate a tool-catalog audit JSON against the schema in 02-output-contract.xml.

Inputs:
    --file PATH       path to audit JSON
    --self-test       run built-in fixtures
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

NAME_RE = re.compile(r"^[a-z][a-z0-9_]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
AXES = ("use_when", "not_use_when", "input_contract", "output_contract", "side_effects")
VERDICTS = {"ok", "rewrite", "split"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("catalog_version", "audited_at", "tools"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "audited_at" in obj and not DATE_RE.match(str(obj["audited_at"])):
        errs.append("audited_at must be ISO date")
    tools = obj.get("tools") or []
    if not isinstance(tools, list):
        errs.append("tools must be list")
        return errs
    for i, t in enumerate(tools):
        for k in ("name", "tokens", "scores", "verdict"):
            if k not in t:
                errs.append(f"tools[{i}] missing {k}")
        if "name" in t and not NAME_RE.match(t["name"]):
            errs.append(f"tools[{i}].name must match {NAME_RE.pattern}")
        if "tokens" in t and (not isinstance(t["tokens"], int) or not (0 <= t["tokens"] <= 500)):
            errs.append(f"tools[{i}].tokens must be int in [0,500]")
        scores = t.get("scores") or {}
        for ax in AXES:
            if ax not in scores:
                errs.append(f"tools[{i}].scores missing {ax}")
            elif scores[ax] not in (0, 1):
                errs.append(f"tools[{i}].scores.{ax} must be 0 or 1")
        if t.get("verdict") not in VERDICTS:
            errs.append(f"tools[{i}].verdict must be one of {sorted(VERDICTS)}")
    return errs


OK = {
    "catalog_version": "1.4.2",
    "audited_at": "2026-05-22",
    "tools": [
        {"name": "search_docs", "tokens": 88,
         "scores": {"use_when": 1, "not_use_when": 1, "input_contract": 1, "output_contract": 1, "side_effects": 1},
         "verdict": "ok"},
    ],
}
BAD = {"tools": [{"name": "X"}]}


def self_test() -> int:
    if validate(OK):
        sys.stderr.write("ok rejected\n"); return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n"); return 1
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
        ap.print_help()
        return 2
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
