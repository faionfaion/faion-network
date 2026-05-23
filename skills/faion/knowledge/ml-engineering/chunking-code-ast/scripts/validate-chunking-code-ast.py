#!/usr/bin/env python3
"""validate-chunking-code-ast — verify code-chunk JSONL against schema + invariants.

Inputs: argv[1] = path to JSONL.
Flags: --help, --self-test.
Exit: 0 pass, 1 fail, 2 cli misuse.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_TYPE = {"function", "async_function", "class", "method", "arrow_function", "code_block"}
ALLOWED_LANG = {"python", "javascript", "typescript", "generic"}
ALLOWED_STRATEGY = {"ast", "tree-sitter", "regex", "generic"}
ID_RE = re.compile(r"^[a-f0-9]{32}$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def validate(records: list[dict]) -> list[str]:
    errors: list[str] = []
    for i, r in enumerate(records):
        for key in ("id", "text", "type", "language", "source", "start_line", "end_line", "strategy", "version"):
            if key not in r:
                errors.append(f"line {i}: missing {key}")
        if "id" in r and not ID_RE.match(str(r["id"])):
            errors.append(f"line {i}: id must be md5 hex")
        if r.get("type") not in ALLOWED_TYPE:
            errors.append(f"line {i}: type {r.get('type')!r} not in allowed")
        if r.get("language") not in ALLOWED_LANG:
            errors.append(f"line {i}: language {r.get('language')!r} not in allowed")
        if r.get("strategy") not in ALLOWED_STRATEGY:
            errors.append(f"line {i}: strategy {r.get('strategy')!r} not in allowed")
        if "version" in r and not SEMVER_RE.match(str(r["version"])):
            errors.append(f"line {i}: version not semver")
        if isinstance(r.get("start_line"), int) and isinstance(r.get("end_line"), int):
            if r["start_line"] > r["end_line"]:
                errors.append(f"line {i}: start_line > end_line")
    return errors


def _self_test() -> int:
    good = {
        "id": "a" * 32, "text": "x", "type": "function", "name": "f", "docstring": "",
        "start_line": 1, "end_line": 2, "language": "python", "source": "x.py",
        "strategy": "ast", "version": "1.0.0", "fallback": False,
    }
    if validate([good]):
        return 1
    bad = {**good, "type": "snippet"}
    if not validate([bad]):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) != 2:
        sys.stderr.write("usage: validate-chunking-code-ast.py <chunks.jsonl>\n")
        return 2
    records = [json.loads(ln) for ln in Path(argv[1]).read_text(encoding="utf-8").splitlines() if ln.strip()]
    errors = validate(records)
    if errors:
        for e in errors:
            sys.stderr.write(f"ERROR: {e}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
