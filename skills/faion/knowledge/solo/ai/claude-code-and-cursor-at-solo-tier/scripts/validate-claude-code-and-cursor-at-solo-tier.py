#!/usr/bin/env python3
"""validate-claude-code-and-cursor-at-solo-tier.py

Validate the artefact for the claude-code-and-cursor-at-solo-tier methodology against the schema in
02-output-contract.xml.

Inputs:
    --file PATH       path to artefact JSON
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
import sys
from pathlib import Path

REQUIRED = ['repo', 'primary_tool', 'model_routing', 'context_budget_tokens', 'spec_before_code']


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("spec_before_code") is not True:
        errs.append("spec_before_code must be true")
    cbt = obj.get("context_budget_tokens")
    if isinstance(cbt, int) and cbt > 2000:
        errs.append(f"context_budget_tokens > 2000: {cbt}")

    return errs


OK = {   'repo': 'github.com/operator/saas-app',
    'primary_tool': 'claude-code',
    'secondary_tool': 'cursor',
    'model_routing': {'design': 'opus', 'routine': 'sonnet', 'mechanical': 'haiku'},
    'context_budget_tokens': 1800,
    'convention_files': ['CLAUDE.md', 'AGENTS.md', 'CONVENTIONS.md'],
    'spec_before_code': True}
BAD = {'repo': 'x', 'primary_tool': 'copilot', 'spec_before_code': False}


def self_test() -> int:
    errs_ok = validate(OK)
    if errs_ok:
        sys.stderr.write(f"ok rejected: {errs_ok}\n")
        return 1
    if not validate(BAD):
        sys.stderr.write("bad accepted\n")
        return 1
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
        sys.stderr.write(f"not a file: {p}\n")
        return 2
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
