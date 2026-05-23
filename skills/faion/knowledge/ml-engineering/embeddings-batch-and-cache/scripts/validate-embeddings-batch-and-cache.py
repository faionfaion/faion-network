#!/usr/bin/env python3
"""validate-embeddings-batch-and-cache.py

Validate an embedding batch+cache config JSON.

Inputs:  --file PATH | --self-test | --help
Exit:    0=valid 1=invalid 2=usage/unreadable
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ID_RE = re.compile(r"^ebc-[a-z0-9-]{6,}$")
VER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PROVIDERS = {"openai", "voyage", "cohere", "mistral", "local-sentence-transformers"}
PROVIDER_LIMIT = {"openai": 2048, "voyage": 128, "cohere": 96, "mistral": 512, "local-sentence-transformers": 4096}
CACHE_BACKENDS = {"redis", "sqlite", "memory", "none"}
KEY_SCHEMES = {"sha256-text-model-dim"}
RETRY_STRAT = {"exponential-jitter", "linear", "none"}


def validate(obj: dict) -> list[str]:
    errs: list[str] = []
    for k in ("artefact_id", "provider", "batch", "cache", "dedup", "retry", "preserve_order", "version", "last_reviewed"):
        if k not in obj:
            errs.append(f"missing required: {k}")
    if "artefact_id" in obj and not ID_RE.match(str(obj["artefact_id"])):
        errs.append("artefact_id pattern fail")
    prov = obj.get("provider")
    if prov not in PROVIDERS:
        errs.append(f"provider must be one of {sorted(PROVIDERS)}")
    batch = obj.get("batch") or {}
    bs = batch.get("size")
    if not isinstance(bs, int) or not (1 <= bs <= 4096):
        errs.append("batch.size must be int in [1,4096]")
    if prov in PROVIDER_LIMIT and isinstance(bs, int) and bs > PROVIDER_LIMIT[prov]:
        errs.append(f"batch.size {bs} exceeds {prov} limit {PROVIDER_LIMIT[prov]} (rule batch-by-provider-limit)")
    bc = batch.get("concurrency")
    if not isinstance(bc, int) or not (1 <= bc <= 64):
        errs.append("batch.concurrency must be int in [1,64]")
    cache = obj.get("cache") or {}
    if cache.get("enabled"):
        if cache.get("backend") not in CACHE_BACKENDS - {"none"}:
            errs.append(f"cache.backend must be one of {sorted(CACHE_BACKENDS - {'none'})}")
        if cache.get("key_scheme") not in KEY_SCHEMES:
            errs.append(f"cache.key_scheme must be one of {sorted(KEY_SCHEMES)} (rule content-hash-cache-key)")
        ttl = cache.get("ttl_seconds")
        if ttl is not None and (not isinstance(ttl, int) or not (60 <= ttl <= 31536000)):
            errs.append("cache.ttl_seconds must be int in [60,31536000]")
    if not isinstance(obj.get("dedup"), bool):
        errs.append("dedup must be bool")
    if not isinstance(obj.get("preserve_order"), bool):
        errs.append("preserve_order must be bool")
    if obj.get("preserve_order") is False:
        errs.append("preserve_order=false violates rule preserve-input-order")
    retry = obj.get("retry") or {}
    if not retry.get("enabled"):
        errs.append("retry.enabled must be true (rule exponential-backoff)")
    if retry.get("strategy") not in RETRY_STRAT:
        errs.append(f"retry.strategy must be one of {sorted(RETRY_STRAT)}")
    if "version" in obj and not VER_RE.match(str(obj["version"])):
        errs.append("version must be semver")
    if "last_reviewed" in obj and not DATE_RE.match(str(obj["last_reviewed"])):
        errs.append("last_reviewed must be ISO date")
    return errs


VALID = {
    "artefact_id": "ebc-news",
    "provider": "openai",
    "model_id": "text-embedding-3-small",
    "dimension": 1536,
    "batch": {"size": 2048, "concurrency": 4},
    "cache": {"enabled": True, "backend": "redis", "key_scheme": "sha256-text-model-dim", "ttl_seconds": 2592000},
    "dedup": True,
    "preserve_order": True,
    "retry": {"enabled": True, "max_attempts": 5, "strategy": "exponential-jitter"},
    "version": "1.1.0",
    "last_reviewed": "2026-05-22",
}

INVALID = {
    "artefact_id": "x",
    "provider": "openai",
    "batch": {"size": 5000, "concurrency": 0},
    "cache": {"enabled": True, "backend": "redis", "key_scheme": "sha256-text"},
    "dedup": False,
    "preserve_order": False,
    "retry": {"enabled": False, "max_attempts": 0, "strategy": "none"},
}


def self_test() -> int:
    if validate(VALID):
        sys.stderr.write(f"self-test FAILED: valid rejected: {validate(VALID)}\n")
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
