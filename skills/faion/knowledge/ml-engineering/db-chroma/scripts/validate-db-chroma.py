#!/usr/bin/env python3
"""validate-db-chroma — verify ChromaStore search response JSON.

Inputs: argv[1] = response JSON.
Flags: --help, --self-test.
Exit: 0 pass, 1 fail, 2 cli misuse.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_METRIC = {"cosine", "l2", "ip"}


def validate(resp: dict) -> list[str]:
    errors: list[str] = []
    for key in ("collection", "metric", "top_k", "hits"):
        if key not in resp:
            errors.append(f"missing {key}")
    if resp.get("metric") not in ALLOWED_METRIC:
        errors.append(f"metric {resp.get('metric')!r} not in allowed")
    tk = resp.get("top_k", 0)
    if not isinstance(tk, int) or tk < 1:
        errors.append("top_k must be int >= 1")
    for i, h in enumerate(resp.get("hits", [])):
        if not isinstance(h.get("id"), str) or not h["id"]:
            errors.append(f"hits[{i}].id must be non-empty string")
        if "payload" not in h:
            errors.append(f"hits[{i}] missing payload")
    return errors


def _self_test() -> int:
    good = {"collection": "documents", "metric": "cosine", "top_k": 1,
            "hits": [{"id": "1", "score": 0.9, "payload": {}}]}
    if validate(good):
        return 1
    if not validate({**good, "metric": "dot"}):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) != 2:
        sys.stderr.write("usage: validate-db-chroma.py <response.json>\n")
        return 2
    resp = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    errors = validate(resp)
    if errors:
        for e in errors:
            sys.stderr.write(f"ERROR: {e}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
