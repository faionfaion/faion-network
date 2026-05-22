#!/usr/bin/env python3
"""validate-db-qdrant — verify QdrantStore search response JSON.

Inputs: argv[1] = response JSON.
Flags: --help, --self-test.
Exit: 0 pass, 1 fail, 2 cli misuse.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_DIST = {"Cosine", "Dot", "Euclid", "Manhattan"}
ALLOWED_QUANT = {"none", "scalar", "binary"}


def validate(resp: dict) -> list[str]:
    errors: list[str] = []
    for key in ("collection", "distance", "top_k", "hits", "payload_indexes_used"):
        if key not in resp:
            errors.append(f"missing {key}")
    if resp.get("distance") not in ALLOWED_DIST:
        errors.append(f"distance {resp.get('distance')!r} not in allowed")
    q = resp.get("quantization")
    if q is not None and q not in ALLOWED_QUANT:
        errors.append(f"quantization {q!r} not in allowed")
    if not isinstance(resp.get("payload_indexes_used"), list):
        errors.append("payload_indexes_used must be list")
    for i, h in enumerate(resp.get("hits", [])):
        for k in ("id", "score", "payload"):
            if k not in h:
                errors.append(f"hits[{i}] missing {k}")
    return errors


def _self_test() -> int:
    good = {"collection": "c", "distance": "Cosine", "top_k": 1,
            "hits": [{"id": 1, "score": 0.9, "payload": {}}],
            "payload_indexes_used": ["category"]}
    if validate(good):
        return 1
    if not validate({**good, "distance": "magic"}):
        return 1
    return 0


def main(argv: list[str]) -> int:
    if "--help" in argv:
        sys.stdout.write(__doc__ or "")
        return 0
    if "--self-test" in argv:
        return _self_test()
    if len(argv) != 2:
        sys.stderr.write("usage: validate-db-qdrant.py <response.json>\n")
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
