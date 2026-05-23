#!/usr/bin/env python3
"""validate-context-window-curation-for-coding-agents.py

Validate a per-task context bundle JSON against schema + budget + caller-cap rules.

Inputs:
    --file PATH      path to bundle JSON
    --self-test      run built-in valid + invalid fixtures
    --help           this message

Exit codes:
    0 = valid
    1 = invalid (violation list printed to stderr)
    2 = usage / unreadable file
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^ctx-[a-z0-9-]{6,}$")
ROLES = {"target", "caller", "type", "agents-md", "glossary", "test-fixture", "config"}
VERDICTS = {"commit-bundle", "block-no-scope", "block-over-budget", "block-no-agents-md"}
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MAX_CALLERS = 2


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "task_id", "task_description", "files", "agents_md_included", "glossary", "exclusions", "total_tokens", "budget_tokens", "verdict", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")

    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^ctx-[a-z0-9-]{6,}$")
    if not isinstance(obj.get("task_description"), str) or len(obj.get("task_description", "")) < 10:
        errs.append("task_description must be string of length >= 10")

    files = obj.get("files") or []
    if not isinstance(files, list) or len(files) < 1:
        errs.append("files must be a non-empty list")
    else:
        caller_count = 0
        for i, f in enumerate(files):
            for sub in ("path", "role", "tokens"):
                if sub not in f:
                    errs.append(f"files[{i}].{sub} missing")
            if f.get("role") not in ROLES:
                errs.append(f"files[{i}].role must be one of {sorted(ROLES)}")
            if not isinstance(f.get("tokens"), int) or not (0 <= f.get("tokens", -1) <= 50000):
                errs.append(f"files[{i}].tokens must be int in [0,50000]")
            if f.get("role") == "caller":
                caller_count += 1
        if caller_count > MAX_CALLERS:
            errs.append(f"more than {MAX_CALLERS} files with role=caller (r1 violation)")

    if not isinstance(obj.get("agents_md_included"), bool):
        errs.append("agents_md_included must be boolean")
    if not isinstance(obj.get("glossary"), str) or len(obj.get("glossary", "")) < 50:
        errs.append("glossary must be string of length >= 50")
    exc = obj.get("exclusions") or []
    if not isinstance(exc, list) or len(exc) < 1:
        errs.append("exclusions must be a non-empty list (r5)")

    tt = obj.get("total_tokens")
    bt = obj.get("budget_tokens")
    if not isinstance(tt, int) or tt < 0:
        errs.append("total_tokens must be non-negative int")
    if not isinstance(bt, int) or bt < 1000:
        errs.append("budget_tokens must be int >= 1000")
    if isinstance(tt, int) and isinstance(bt, int) and tt > bt:
        errs.append("total_tokens > budget_tokens (r3 violation)")

    verdict = obj.get("verdict")
    if verdict and verdict not in VERDICTS:
        errs.append(f"verdict must be one of {sorted(VERDICTS)}")
    if verdict == "commit-bundle":
        if not obj.get("agents_md_included"):
            errs.append("verdict=commit-bundle requires agents_md_included=true (r2)")
        if isinstance(tt, int) and isinstance(bt, int) and tt > bt:
            errs.append("verdict=commit-bundle requires total_tokens <= budget_tokens")

    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver MAJOR.MINOR.PATCH")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date YYYY-MM-DD")
    return errs


VALID_FIXTURE = {
    "artefact_id": "ctx-task-4421",
    "task_id": "TICKET-4421",
    "task_description": "Add /v2/quote endpoint with FX rounding fixed",
    "files": [
        {"path": "AGENTS.md", "role": "agents-md", "tokens": 1200},
        {"path": "src/orders/quote.py", "role": "target", "tokens": 1500},
        {"path": "src/orders/types.py", "role": "type", "tokens": 600},
        {"path": "src/api/router.py", "role": "caller", "tokens": 900},
    ],
    "agents_md_included": True,
    "glossary": "FX = foreign exchange; round-half-up = banker rounding alternative; shadow = dark-launch.",
    "exclusions": ["tests/", "migrations/", "vendor/", "generated/"],
    "total_tokens": 4200,
    "budget_tokens": 6000,
    "verdict": "commit-bundle",
    "version": "1.0.0",
    "last_reviewed": "2026-05-23",
}

INVALID_FIXTURE = {
    "artefact_id": "ctx",
    "task_id": "x",
    "task_description": "fix it",
    "files": [{"path": "everything.py", "role": "all", "tokens": 60000}],
    "agents_md_included": False,
    "glossary": "",
    "exclusions": [],
    "total_tokens": 60000,
    "budget_tokens": 6000,
    "verdict": "commit-bundle",
    "version": "1.0",
    "last_reviewed": "today",
}


def self_test() -> int:
    errs = validate(VALID_FIXTURE)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid fixture rejected: {errs}\n")
        return 1
    errs = validate(INVALID_FIXTURE)
    if not errs:
        sys.stderr.write("self-test FAILED: invalid fixture accepted\n")
        return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str, help="path to bundle JSON")
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
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
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
