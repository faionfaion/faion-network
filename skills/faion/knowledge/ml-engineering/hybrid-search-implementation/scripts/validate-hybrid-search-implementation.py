#!/usr/bin/env python3
"""validate-hybrid-search-implementation.

Validates a hybrid-search-result JSON file against the 02-output-contract schema.

Inputs:  --input PATH    path to result JSON
Outputs: stdout JSON {"ok": bool, "violations": [...]}
Exit:    0 pass, 1 fail
Flags:   --self-test    built-in fixture; --help    print help
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BACKENDS = {"weaviate", "qdrant", "pinecone", "elasticsearch", "custom"}
FUSIONS = {"rrf", "linear"}


def validate(d: dict) -> list[str]:
    v: list[str] = []
    for key in ("query", "backend", "fusion", "results"):
        if key not in d:
            v.append(f"missing:{key}")
    if d.get("backend") not in BACKENDS:
        v.append(f"bad-backend:{d.get('backend')}")
    if d.get("fusion") not in FUSIONS:
        v.append(f"bad-fusion:{d.get('fusion')}")
    rs = d.get("results", [])
    if not isinstance(rs, list):
        v.append("results-not-list")
    else:
        for i, r in enumerate(rs):
            for k in ("id", "score", "dense_rank", "sparse_rank"):
                if k not in r:
                    v.append(f"result[{i}]-missing:{k}")
    return v


def _self_test() -> int:
    good = {"query": "q", "backend": "qdrant", "fusion": "rrf",
            "results": [{"id": "x", "score": 0.1, "dense_rank": 1, "sparse_rank": 2}]}
    bad = {"query": "q", "results": [{"id": "x"}]}
    return 0 if not validate(good) and validate(bad) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if not args.input:
        ap.print_help()
        return 1
    d = json.loads(args.input.read_text(encoding="utf-8"))
    violations = validate(d)
    sys.stdout.write(json.dumps({"ok": not violations, "violations": violations}, indent=2) + "\n")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
