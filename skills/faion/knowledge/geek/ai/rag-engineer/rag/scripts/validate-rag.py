#!/usr/bin/env python3
"""validate-rag.

Validates a RAG answer JSON against 02-output-contract schema.

Inputs:  --input PATH    path to RAG answer JSON
Outputs: stdout JSON {"ok": bool, "violations": [...]}
Exit:    0 pass, 1 fail
Flags:   --self-test    built-in fixture
         --help          print help
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(d: dict) -> list[str]:
    v: list[str] = []
    for key in ("query", "answer", "citations", "retrieval", "faithfulness"):
        if key not in d:
            v.append(f"missing:{key}")
    if not isinstance(d.get("citations", []), list):
        v.append("citations-not-list")
    else:
        for i, c in enumerate(d.get("citations", [])):
            for k in ("source", "page", "chunk_id", "validated"):
                if k not in c:
                    v.append(f"citation[{i}]-missing:{k}")
    r = d.get("retrieval", {})
    if not isinstance(r, dict):
        v.append("retrieval-not-object")
    else:
        for k in ("top_k", "rerank_top_k", "latency_ms"):
            if k not in r:
                v.append(f"retrieval-missing:{k}")
    f = d.get("faithfulness")
    if not isinstance(f, (int, float)) or not (0 <= f <= 1):
        v.append("faithfulness-out-of-range")
    return v


def _self_test() -> int:
    good = {"query": "q", "answer": "a [Source: x, page 1]", "citations": [{"source": "x", "page": 1, "chunk_id": "c1", "validated": True}], "retrieval": {"top_k": 20, "rerank_top_k": 5, "latency_ms": 100}, "faithfulness": 0.95}
    bad = {"query": "q", "answer": "a"}
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
