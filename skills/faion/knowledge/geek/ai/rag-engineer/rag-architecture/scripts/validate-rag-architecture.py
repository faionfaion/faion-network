#!/usr/bin/env python3
"""validate-rag-architecture.

Validates a RAG architecture decision record JSON against 02-output-contract schema.

Inputs:  --input PATH    record JSON path
Outputs: stdout JSON {"ok": bool, "violations": [...]}
Exit:    0 pass, 1 fail
Flags:   --self-test    fixture
         --help          print help
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CHUNK_STRATS = {"fixed", "sentence", "paragraph", "semantic", "header"}
DBS = {"qdrant", "weaviate", "chroma", "pgvector", "pinecone", "milvus"}
MODES = {"vector", "hybrid"}
ORDS = {"relevance", "recency", "source"}


def validate(d: dict) -> list[str]:
    v: list[str] = []
    for k in ("chunking", "embeddings", "vector_db", "retrieval", "context", "metrics", "signoff"):
        if k not in d:
            v.append(f"missing:{k}")
    c = d.get("chunking", {})
    if c.get("strategy") not in CHUNK_STRATS:
        v.append(f"bad-chunk-strat:{c.get('strategy')}")
    if d.get("vector_db") not in DBS:
        v.append(f"bad-db:{d.get('vector_db')}")
    r = d.get("retrieval", {})
    if r.get("mode") not in MODES:
        v.append(f"bad-retrieval-mode:{r.get('mode')}")
    ctx = d.get("context", {})
    if ctx.get("ordering") not in ORDS:
        v.append(f"bad-ordering:{ctx.get('ordering')}")
    m = d.get("metrics", {})
    for mk in ("mrr_target", "faithfulness_target", "latency_p95_ms", "cost_per_query_usd"):
        if mk not in m:
            v.append(f"metrics-missing:{mk}")
    s = d.get("signoff", {})
    for sk in ("owner", "date"):
        if sk not in s:
            v.append(f"signoff-missing:{sk}")
    return v


def _self_test() -> int:
    good = {"chunking": {"strategy": "header", "size": 1024, "overlap": 200}, "embeddings": {"model": "e", "dim": 3072}, "vector_db": "qdrant", "retrieval": {"mode": "hybrid", "top_k_pool": 20, "top_k_rerank": 5}, "context": {"budget_tokens": 5000, "ordering": "relevance"}, "metrics": {"mrr_target": 0.7, "faithfulness_target": 0.9, "latency_p95_ms": 1500, "cost_per_query_usd": 0.01}, "signoff": {"owner": "a", "date": "2026-05-22"}}
    bad = {"chunking": {"strategy": "fixed"}, "vector_db": "qdrant"}
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
