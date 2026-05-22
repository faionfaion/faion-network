#!/usr/bin/env python3
"""validate-vector-databases.py — validate vector-db.yaml.

Inputs: --file PATH | --self-test | --help
Exit:   0 valid, 1 invalid, 2 usage
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore

REQUIRED = ["kind", "connection", "collection", "multi_tenant", "hybrid_search"]
KINDS = {"qdrant", "weaviate", "milvus", "pgvector", "pinecone", "chroma"}
METRICS = {"cosine", "dot", "euclidean"}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    if obj.get("kind") not in KINDS:
        errs.append(f"kind must be in {sorted(KINDS)}")
    coll = obj.get("collection", {})
    if isinstance(coll, dict):
        if coll.get("metric") not in METRICS:
            errs.append("collection.metric must be cosine|dot|euclidean (r5-metric-matches-embedding)")
        em = coll.get("embedding_model", {})
        if not isinstance(em, dict) or not em.get("version"):
            errs.append("collection.embedding_model.version must be pinned (r2-pin-embedding-model)")
        if not (32 <= coll.get("dim", 0) <= 4096):
            errs.append("collection.dim out of [32, 4096]")
    mt = obj.get("multi_tenant", {})
    if isinstance(mt, dict) and mt.get("enabled") and not mt.get("filter_field"):
        errs.append("multi_tenant.filter_field required when enabled (r3-tenant-filter-required)")
    if obj.get("kind") == "chroma":
        errs.append("Chroma is dev-only; pick another DB for production (fm-01)")
    return errs


FIXTURE_VALID = """
kind: qdrant
connection: {host: x.local, port: 6333}
collection:
  name: kb
  dim: 1024
  metric: cosine
  embedding_model: {name: voyage-3-large, version: "2026-04"}
multi_tenant: {enabled: true, filter_field: tenant_id}
hybrid_search: {enabled: true, fusion: rrf}
"""

FIXTURE_INVALID = """
kind: chroma
connection: {}
collection: {name: x, dim: 8, metric: hamming, embedding_model: {name: foo}}
multi_tenant: {enabled: true}
hybrid_search: {enabled: false}
"""


def self_test() -> int:
    if yaml is None:
        sys.stderr.write("pyyaml required\n"); return 2
    if validate(yaml.safe_load(FIXTURE_VALID)):
        sys.stderr.write("valid fixture rejected\n"); return 1
    errs = validate(yaml.safe_load(FIXTURE_INVALID))
    if not errs:
        sys.stderr.write("invalid fixture accepted\n"); return 1
    sys.stdout.write(f"self-test OK ({len(errs)} violations on invalid)\n")
    return 0


def load(p: Path) -> object:
    raw = p.read_text(encoding="utf-8")
    if p.suffix in (".yml", ".yaml"):
        if yaml is None:
            raise RuntimeError("pyyaml required")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(prog="validate-vector-databases", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", type=str)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.file:
        ap.print_help(); return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n"); return 2
    try:
        obj = load(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n"); return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
