#!/usr/bin/env python3
"""validate-embedding-generation.py

Validate an embedding-producer config JSON.

Inputs:
    --file PATH    path to producer-config JSON
    --self-test    run built-in fixtures
    --help         this message

Exit codes: 0=valid, 1=invalid, 2=usage/unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^emp-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PROVIDERS = {"openai", "voyage", "cohere", "mistral", "local-sentence-transformers"}
BATCH_MODES = {"sync", "async-parallel", "batch-api"}
CACHE_BACKENDS = {"redis", "sqlite", "memory", "none"}
KEY_SCHEMES = {"sha256-text-model-dim"}
RETRY_STRAT = {"exponential-jitter", "linear", "none"}
STORE_KINDS = {"qdrant", "pgvector", "pinecone", "weaviate", "chroma"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "model_id", "dimension", "normalize", "batch", "cache", "retry", "store", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id must match ^emp-[a-z0-9-]{6,}$")
    if "provider" in obj and obj["provider"] not in PROVIDERS:
        errs.append(f"provider must be one of {sorted(PROVIDERS)}")
    dim = obj.get("dimension")
    if not isinstance(dim, int) or not (64 <= dim <= 8192):
        errs.append("dimension must be int in [64,8192]")
    if "normalize" in obj and not isinstance(obj["normalize"], bool):
        errs.append("normalize must be bool")
    batch = obj.get("batch") or {}
    if batch.get("mode") not in BATCH_MODES:
        errs.append(f"batch.mode must be one of {sorted(BATCH_MODES)}")
    bs = batch.get("size")
    if not isinstance(bs, int) or not (1 <= bs <= 4096):
        errs.append("batch.size must be int in [1,4096]")
    cache = obj.get("cache") or {}
    if cache.get("enabled"):
        if cache.get("backend") not in CACHE_BACKENDS - {"none"}:
            errs.append(f"cache.backend must be one of {sorted(CACHE_BACKENDS - {'none'})} when enabled")
        if cache.get("key_scheme") not in KEY_SCHEMES:
            errs.append(f"cache.key_scheme must be one of {sorted(KEY_SCHEMES)} (rule content-hash-cache)")
    retry = obj.get("retry") or {}
    if not retry.get("enabled"):
        errs.append("retry.enabled must be true (rule exponential-backoff-retry)")
    if retry.get("strategy") not in RETRY_STRAT:
        errs.append(f"retry.strategy must be one of {sorted(RETRY_STRAT)}")
    if retry.get("strategy") == "none" and retry.get("enabled"):
        errs.append("retry.strategy=none contradicts enabled=true")
    store = obj.get("store") or {}
    if store.get("kind") not in STORE_KINDS:
        errs.append(f"store.kind must be one of {sorted(STORE_KINDS)}")
    sd = store.get("schema_dimension")
    if not isinstance(sd, int) or not (64 <= sd <= 8192):
        errs.append("store.schema_dimension must be int in [64,8192]")
    if isinstance(dim, int) and isinstance(sd, int) and dim != sd:
        errs.append(f"dimension {dim} != store.schema_dimension {sd} (rule dimension-locked-schema)")
    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


VALID = {
    "artefact_id": "emp-news-rewrite",
    "model_id": "text-embedding-3-small",
    "provider": "openai",
    "dimension": 1536,
    "normalize": True,
    "batch": {"mode": "async-parallel", "size": 1024, "concurrency": 4},
    "cache": {"enabled": True, "backend": "redis", "key_scheme": "sha256-text-model-dim"},
    "retry": {"enabled": True, "max_attempts": 5, "strategy": "exponential-jitter"},
    "store": {"kind": "qdrant", "collection": "news-chunks", "schema_dimension": 1536},
    "version": "1.1.0",
    "last_reviewed": "2026-05-22",
}

INVALID = {
    "artefact_id": "x",
    "model_id": "?",
    "dimension": 1024,
    "normalize": False,
    "batch": {"mode": "sync", "size": 0},
    "cache": {"enabled": True, "backend": "redis", "key_scheme": "sequential-id"},
    "retry": {"enabled": False, "max_attempts": 1, "strategy": "none"},
    "store": {"kind": "qdrant", "collection": "x", "schema_dimension": 512},
}


def self_test() -> int:
    errs = validate(VALID)
    if errs:
        sys.stderr.write(f"self-test FAILED: valid rejected: {errs}\n")
        return 1
    if not validate(INVALID):
        sys.stderr.write("self-test FAILED: invalid accepted\n")
        return 1
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
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.is_file():
        sys.stderr.write(f"not a file: {p}\n")
        return 2
    try:
        obj = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        sys.stderr.write(f"invalid JSON: {e}\n")
        return 2
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
