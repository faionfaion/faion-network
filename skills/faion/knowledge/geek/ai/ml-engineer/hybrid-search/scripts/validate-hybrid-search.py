#!/usr/bin/env python3
"""validate-hybrid-search.py — validate hybrid-search-config.json.

Inputs: --file PATH | --self-test | --help
Exit codes: 0 valid; 1 invalid; 2 usage.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REQUIRED = ["artefact_id", "version", "last_reviewed", "vector_db", "fusion", "rerank", "metrics"]
DBS = {"qdrant", "weaviate", "pinecone", "elasticsearch", "pgvector", "mongodb-atlas"}
METHODS = {"rrf", "linear"}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing field: {k}")
    if "version" in obj and not SEMVER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be YYYY-MM-DD")
    if obj.get("vector_db") not in DBS:
        errs.append("vector_db not in enum")
    fusion = obj.get("fusion", {})
    if fusion.get("method") not in METHODS:
        errs.append("fusion.method not in enum")
    rerank = obj.get("rerank", {})
    if "enabled" not in rerank or not isinstance(rerank["enabled"], bool):
        errs.append("rerank.enabled missing/non-bool")
    metrics = obj.get("metrics", {})
    if "precision_at_10" not in metrics or "p99_latency_ms" not in metrics:
        errs.append("metrics incomplete")
    return errs


VALID_FIX = {
    "artefact_id": "x", "version": "1.0.0", "last_reviewed": "2026-05-22",
    "vector_db": "qdrant", "fusion": {"method": "rrf"},
    "rerank": {"enabled": False},
    "metrics": {"precision_at_10": 0.9, "p99_latency_ms": 50},
}
INVALID_FIX: dict = {}


def self_test() -> int:
    if validate(VALID_FIX):
        sys.stderr.write("valid rejected\n"); return 1
    if not validate(INVALID_FIX):
        sys.stderr.write("invalid accepted\n"); return 1
    sys.stdout.write("self-test OK\n")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    errs = validate(json.loads(p.read_text()))
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
