#!/usr/bin/env python3
"""validate-chunking-document-structure — verify doc-structure chunks JSONL.

Inputs: argv[1] = path to JSONL.
Flags: --help, --self-test.
Exit: 0 pass, 1 fail, 2 cli misuse.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_STRATEGY = {"markdown", "html"}
ID_RE = re.compile(r"^[a-f0-9]{32}$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def validate(records: list[dict]) -> list[str]:
    errors: list[str] = []
    for i, r in enumerate(records):
        for key in ("id", "text", "header_path", "token_count", "source", "strategy", "version"):
            if key not in r:
                errors.append(f"line {i}: missing {key}")
        if "id" in r and not ID_RE.match(str(r["id"])):
            errors.append(f"line {i}: id must be md5 hex")
        tc = r.get("token_count")
        if not isinstance(tc, int) or tc < 1 or tc > 4000:
            errors.append(f"line {i}: token_count out of [1,4000]")
        if r.get("strategy") not in ALLOWED_STRATEGY:
            errors.append(f"line {i}: strategy {r.get('strategy')!r} not in allowed")
        if "version" in r and not SEMVER_RE.match(str(r["version"])):
            errors.append(f"line {i}: version not semver")
    return errors


def _self_test() -> int:
    good = {"id": "a"*32, "text": "h\n\nbody", "header_path": "h", "token_count": 2,
            "source": "x.md", "strategy": "markdown", "version": "1.0.0", "part_index": None}
    if validate([good]):
        return 1
    if not validate([{**good, "strategy": "regex"}]):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) != 2:
        sys.stderr.write("usage: validate-chunking-document-structure.py <chunks.jsonl>\n")
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
