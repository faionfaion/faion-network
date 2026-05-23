#!/usr/bin/env python3
"""Validate embedding-pipeline-config artefact.

USAGE:
    validate-embedding-applications.py <input.json>
    validate-embedding-applications.py --self-test
    validate-embedding-applications.py --help

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
METRICS = {"cosine", "dot_product", "l2"}
METADATA_REQUIRED = {"model_name", "model_version"}


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    if not (c.get("model_name") or "").strip():
        v.append("model_name required")
    if not (c.get("model_version") or "").strip():
        v.append("model_version required")
    if c.get("provider") not in PROVIDERS:
        v.append(f"provider must be one of {sorted(PROVIDERS)}")
    bs = c.get("batch_size")
    if not isinstance(bs, int) or bs < 32 or bs > 2048:
        v.append("batch_size must be in [32,2048] (rule r5)")
    if c.get("normalize") is not True:
        if c.get("metric") == "cosine":
            v.append("cosine metric requires normalize=true (rule r3)")
    if c.get("metric") not in METRICS:
        v.append(f"metric must be one of {sorted(METRICS)}")
    if not (c.get("domain_bench_path") or "").strip():
        v.append("domain_bench_path required (rule r1)")
    rt = c.get("recall10_threshold")
    if not isinstance(rt, (int, float)) or rt < 0.5 or rt > 1.0:
        v.append("recall10_threshold must be in [0.5,1.0] (rule r4)")
    md = set(c.get("vector_metadata_fields") or [])
    if not METADATA_REQUIRED <= md:
        v.append(f"vector_metadata_fields must include {sorted(METADATA_REQUIRED)} (rule r7)")
    return v


GOOD = {
    "model_name": "text-embedding-3-large",
    "model_version": "2026-04",
    "provider": "openai",
    "batch_size": 256,
    "normalize": True,
    "metric": "cosine",
    "domain_bench_path": "git://faion/eval/embed.jsonl",
    "recall10_threshold": 0.7,
    "vector_metadata_fields": ["model_name", "model_version", "created_at"],
}
BAD = {
    "model_name": "",
    "model_version": "",
    "provider": "unknown",
    "batch_size": 5000,
    "normalize": False,
    "metric": "cosine",
    "domain_bench_path": "",
    "recall10_threshold": 0.1,
    "vector_metadata_fields": [],
}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("model_name" in x for x in bad)
    assert any("batch_size" in x for x in bad)
    assert any("normalize" in x for x in bad)
    assert any("recall10" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-embedding-applications.py")
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
