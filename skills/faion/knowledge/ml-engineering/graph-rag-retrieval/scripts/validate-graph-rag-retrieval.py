#!/usr/bin/env python3
"""validate-graph-rag-retrieval.

Validates a graph-rag-retrieval result JSON file against the 02-output-contract.xml schema.

Inputs:  --input PATH   path to a result JSON file
Outputs: stdout JSON {"ok": bool, "violations": [...]}
Exit:    0 on pass, 1 on fail
Flags:   --self-test    run against a built-in fixture
         --help         print this help
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_KEYS = {"query", "query_type", "retrieval_path", "candidates", "assembled_context", "fallback_used"}
QUERY_TYPES = {"GLOBAL", "ENTITY", "RELATIONSHIP", "LOCAL"}
PATHS = {"summary", "entity-neighbors", "shortest-path", "vector-search", "hybrid"}
CAND_SOURCES = {"vector", "graph-neighbor", "shortest-path", "summary"}


def validate(doc: dict) -> list[str]:
    v: list[str] = []
    missing = REQUIRED_KEYS - set(doc)
    if missing:
        v.append(f"missing-keys:{sorted(missing)}")
        return v
    if doc["query_type"] not in QUERY_TYPES:
        v.append(f"bad-query-type:{doc['query_type']}")
    if doc["retrieval_path"] not in PATHS:
        v.append(f"bad-retrieval-path:{doc['retrieval_path']}")
    if not isinstance(doc["candidates"], list):
        v.append("candidates-not-list")
    else:
        for i, c in enumerate(doc["candidates"]):
            if not isinstance(c, dict):
                v.append(f"candidate[{i}]-not-object")
                continue
            for key in ("chunk_id", "score", "source"):
                if key not in c:
                    v.append(f"candidate[{i}]-missing:{key}")
            if c.get("source") and c["source"] not in CAND_SOURCES:
                v.append(f"candidate[{i}]-bad-source:{c['source']}")
    if not isinstance(doc["assembled_context"], str):
        v.append("assembled_context-not-string")
    if not isinstance(doc["fallback_used"], bool):
        v.append("fallback_used-not-bool")
    return v


def _self_test() -> int:
    good = {
        "query": "How is Alice related to Acme?",
        "query_type": "RELATIONSHIP",
        "retrieval_path": "shortest-path",
        "candidates": [{"chunk_id": "c1", "score": 0.9, "source": "shortest-path"}],
        "assembled_context": "Alice -> Acme",
        "fallback_used": False,
    }
    bad = {"query": "q", "candidates": ["c1"]}
    if validate(good):
        return 1
    if not validate(bad):
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, help="result JSON path")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if not args.input:
        ap.print_help()
        return 1
    doc = json.loads(args.input.read_text(encoding="utf-8"))
    violations = validate(doc)
    sys.stdout.write(json.dumps({"ok": not violations, "violations": violations}, indent=2) + "\n")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
