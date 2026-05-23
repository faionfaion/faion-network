#!/usr/bin/env python3
"""validate-chunking-basics — verify chunk JSONL against the schema + invariants.

Inputs:
  argv[1]  path to JSONL file, one chunk per line
Flags:
  --help       print this help and exit 0
  --self-test  run built-in fixture
Exit codes:
  0  all chunks valid
  1  one or more violations
  2  CLI usage error
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ALLOWED_STRATEGY = {"fixed", "sentence", "paragraph", "recursive", "markdown", "code-ast", "html", "semantic"}
ID_RE = re.compile(r"^[a-f0-9]{32}$")
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def validate(records: list[dict]) -> list[str]:
    errors: list[str] = []
    for i, r in enumerate(records):
        for key in ("id", "text", "token_count", "source", "chunk_index", "strategy", "version"):
            if key not in r:
                errors.append(f"line {i}: missing {key}")
        if "id" in r and not ID_RE.match(str(r["id"])):
            errors.append(f"line {i}: id must be md5 hex")
        tc = r.get("token_count")
        if not isinstance(tc, int) or tc < 1 or tc > 4000:
            errors.append(f"line {i}: token_count out of [1,4000]")
        if r.get("strategy") not in ALLOWED_STRATEGY:
            errors.append(f"line {i}: strategy {r.get('strategy')!r} not allowed")
        if "version" in r and not SEMVER_RE.match(str(r["version"])):
            errors.append(f"line {i}: version not semver")
    return errors


def _self_test() -> int:
    good = {
        "id": hashlib.md5(b"x").hexdigest(),
        "text": "hello",
        "token_count": 1,
        "source": "x.md",
        "chunk_index": 0,
        "strategy": "recursive",
        "version": "1.0.0",
    }
    if validate([good]):
        return 1
    bad = {**good, "token_count": 9999, "strategy": "magic"}
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
        sys.stderr.write("usage: validate-chunking-basics.py <chunks.jsonl>\n")
        return 2
    path = Path(argv[1])
    records = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    errors = validate(records)
    if errors:
        for e in errors:
            sys.stderr.write(f"ERROR: {e}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
