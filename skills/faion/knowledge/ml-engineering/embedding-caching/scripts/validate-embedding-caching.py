#!/usr/bin/env python3
"""Validate embedding cache-config artefact.

USAGE:
    validate-embedding-caching.py <input.json>
    validate-embedding-caching.py --self-test
    validate-embedding-caching.py --help

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

BACKENDS = {"redis", "valkey", "dynamodb", "memory"}
COMPONENTS = {"model_name", "model_version", "text"}


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    if c.get("backend") not in BACKENDS:
        v.append(f"backend must be one of {sorted(BACKENDS)}")
    if c.get("hash_algo") != "sha256":
        v.append("hash_algo must be sha256 (rule r1)")
    kc = set(c.get("key_components") or [])
    if "model_version" not in kc:
        v.append("key_components must include model_version (rule r2)")
    if not COMPONENTS <= kc and not (COMPONENTS - kc) == set():
        # ensure all 3 components present
        missing = COMPONENTS - kc
        if missing:
            v.append(f"key_components missing {sorted(missing)} (rule r1+r2)")
    td = c.get("ttl_days")
    if not isinstance(td, int) or td < 1 or td > 365:
        v.append("ttl_days must be int in [1,365] (rule r3)")
    if c.get("emit_hit_metric") is not True:
        v.append("emit_hit_metric must be true (rule r4)")
    return v


GOOD = {"backend": "valkey", "hash_algo": "sha256", "key_components": ["model_name", "model_version", "text"], "ttl_days": 90, "emit_hit_metric": True}
BAD = {"backend": "redis", "hash_algo": "md5", "key_components": ["text"], "ttl_days": 9999, "emit_hit_metric": False}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("hash_algo" in x for x in bad)
    assert any("model_version" in x for x in bad)
    assert any("ttl_days" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-embedding-caching.py")
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
