#!/usr/bin/env python3
"""validate-headless-cli-four-guards.py

Purpose:
    Lint a shell script that invokes claude/codex/aider/opencode and report
    which of the four guards are present and which are missing.

Inputs:
    --file PATH      Shell script to lint
    --self-test      Lint the built-in smoke fixture

Outputs:
    Stdout: JSON lint report
    Exit 0 if all four guards present, 1 if any missing, 2 on usage error.

Dependencies: stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SMOKE = HERE.parent / "templates" / "_smoke-test.sh"

PRINT_FLAGS = [r"(?<![A-Za-z0-9])-p(?![A-Za-z0-9])", r"--print\b", r"\bcodex exec\b", r"--yes\b", r"headless"]
ALLOW_FLAGS = [r"--allowedTools\b", r"--sandbox\b", r"--auto-test\b"]
TURN_FLAGS = [r"--max-turns\b", r"\btimeout\b", r"--max-chat-history-tokens\b"]
STDIN_RE = re.compile(r"<\s*/dev/null")
DANGEROUS_RE = re.compile(r"--dangerously-skip-permissions")


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text) for p in patterns)


def lint(script_text: str, script_path: str) -> dict:
    has_print = has_any(script_text, PRINT_FLAGS)
    has_allow = has_any(script_text, ALLOW_FLAGS) and not DANGEROUS_RE.search(script_text)
    has_turn = has_any(script_text, TURN_FLAGS)
    has_stdin = bool(STDIN_RE.search(script_text))
    present, missing = [], []
    for name, ok in (("print", has_print), ("allowlist", has_allow),
                     ("max_turns", has_turn), ("stdin_closed", has_stdin)):
        (present if ok else missing).append(name)
    if DANGEROUS_RE.search(script_text):
        missing.append("no-dangerously-skip-permissions")
    return {"script_path": script_path, "guards_present": present, "missing_guards": missing}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    p.add_argument("--file", type=Path)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    target = SMOKE if args.self_test else args.file
    if target is None:
        p.error("either --file or --self-test must be given")
    if not target.exists():
        sys.stdout.write(f"FAIL: file not found: {target}\n")
        return 1
    rep = lint(target.read_text(encoding="utf-8"), str(target))
    sys.stdout.write(json.dumps(rep, indent=2) + "\n")
    return 0 if not rep["missing_guards"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
