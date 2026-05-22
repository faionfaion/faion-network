#!/usr/bin/env python3
"""validate-chunking-production-service — verify service envelope JSON.

Inputs: argv[1] = path to envelope JSON.
Flags: --help, --self-test.
Exit: 0 pass, 1 fail, 2 cli misuse.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_REQ = {"fixed","sentence","paragraph","semantic","recursive","markdown","html","code"}
ALLOWED_USED = ALLOWED_REQ | {"fallback"}


def validate(env: dict) -> list[str]:
    errors: list[str] = []
    for key in ("requested_strategy", "strategy_used", "chunk_count", "chunks", "warnings"):
        if key not in env:
            errors.append(f"missing {key}")
    if env.get("requested_strategy") not in ALLOWED_REQ:
        errors.append("requested_strategy not in enum")
    if env.get("strategy_used") not in ALLOWED_USED:
        errors.append("strategy_used not in enum")
    if env.get("strategy_used") == "fallback" and not env.get("warnings"):
        errors.append("fallback without warnings entries")
    for i, c in enumerate(env.get("chunks", [])):
        if "metadata" not in c:
            errors.append(f"chunk {i} missing metadata")
        if "strategy_used" not in c:
            errors.append(f"chunk {i} missing strategy_used")
    return errors


def _self_test() -> int:
    good = {"requested_strategy": "markdown", "strategy_used": "markdown", "chunk_count": 1,
            "chunks": [{"id": "a"*32, "text": "x", "strategy_used": "markdown", "metadata": {}, "version": "1.0.0"}],
            "warnings": []}
    if validate(good):
        return 1
    if not validate({**good, "strategy_used": "fallback"}):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) != 2:
        sys.stderr.write("usage: validate-chunking-production-service.py <envelope.json>\n")
        return 2
    env = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    errors = validate(env)
    if errors:
        for e in errors:
            sys.stderr.write(f"ERROR: {e}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
