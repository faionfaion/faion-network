#!/usr/bin/env python3
"""Validate embedder-config artefact.

USAGE:
    validate-embedding-generation.py <input.json>
    validate-embedding-generation.py --self-test
    validate-embedding-generation.py --help

EXIT CODES:
    0 valid
    1 schema violation
    2 usage / unreadable

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROVIDERS = {"openai", "cohere", "voyage", "google", "azure", "local"}
PROVIDER_CAPS = {"openai": 2048, "cohere": 96, "voyage": 128, "google": 250, "azure": 2048, "local": 1024}


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    if not (c.get("model_name") or "").strip():
        v.append("model_name required (rule r1)")
    if not (c.get("model_version") or "").strip():
        v.append("model_version required (rule r1)")
    p = c.get("provider")
    if p not in PROVIDERS:
        v.append(f"provider must be one of {sorted(PROVIDERS)}")
    bs = c.get("batch_size")
    if not isinstance(bs, int) or bs < 8 or bs > 2048:
        v.append("batch_size must be int in [8,2048]")
    if isinstance(bs, int) and p in PROVIDER_CAPS and bs > PROVIDER_CAPS[p]:
        v.append(f"batch_size {bs} exceeds provider {p!r} cap {PROVIDER_CAPS[p]} (rule r2)")
    if c.get("normalize") is not True:
        v.append("normalize must be true (rule r4)")
    if c.get("cache_hash_algo") != "sha256":
        v.append("cache_hash_algo must be sha256 (rule r3)")
    mt = c.get("max_input_tokens")
    if not isinstance(mt, int) or mt < 1 or mt > 32768:
        v.append("max_input_tokens must be int in [1,32768] (rule r5)")
    if p == "cohere":
        if not (c.get("input_type_index") or "").strip() or not (c.get("input_type_query") or "").strip():
            v.append("Cohere requires input_type_index + input_type_query (rule r6)")
    return v


GOOD = {"model_name": "text-embedding-3-large", "model_version": "2026-04", "provider": "openai", "batch_size": 512, "normalize": True, "cache_hash_algo": "sha256", "max_input_tokens": 8191, "input_type_index": "n/a", "input_type_query": "n/a"}
BAD = {"model_name": "", "model_version": "", "provider": "cohere", "batch_size": 5000, "normalize": False, "cache_hash_algo": "md5", "max_input_tokens": 100000, "input_type_index": "", "input_type_query": ""}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("batch_size" in x for x in bad)
    assert any("cache_hash_algo" in x for x in bad)
    assert any("Cohere requires" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-embedding-generation.py")
    p.add_argument("path", nargs="?")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)
    if args.self_test:
        return _self_test()
    if not args.path:
        p.print_help()
        return 2
    out = validate(json.loads(Path(args.path).read_text()))
    if out:
        for x in out:
            sys.stdout.write(f"VIOLATION: {x}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
