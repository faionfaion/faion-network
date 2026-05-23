#!/usr/bin/env python3
"""Validate model-selection artefact.

USAGE:
    validate-embedding-models.py <input.json>
    validate-embedding-models.py --self-test
    validate-embedding-models.py --help

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

PROVIDERS = {"openai", "cohere", "voyage", "mistral", "google", "azure", "local"}
CORPUS_CLASSES = {"general", "code", "multilingual", "legal", "biomedical"}
METRICS = {"cosine", "dot_product", "l2"}


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    if not (c.get("model_name") or "").strip():
        v.append("model_name required (rule r7)")
    if not (c.get("model_version") or "").strip():
        v.append("model_version required (rule r7)")
    if c.get("provider") not in PROVIDERS:
        v.append(f"provider must be one of {sorted(PROVIDERS)}")
    if c.get("corpus_class") not in CORPUS_CLASSES:
        v.append(f"corpus_class must be one of {sorted(CORPUS_CLASSES)}")
    d = c.get("dim")
    if not isinstance(d, int) or d < 256 or d > 4096:
        v.append("dim must be int in [256,4096]")
    if c.get("metric") not in METRICS:
        v.append(f"metric must be one of {sorted(METRICS)}")
    mteb = c.get("mteb_retrieval_score")
    if not isinstance(mteb, (int, float)) or mteb < 0 or mteb > 1:
        v.append("mteb_retrieval_score must be in [0,1] (rule r8)")
    dr = c.get("domain_recall10")
    if not isinstance(dr, (int, float)) or dr < 0 or dr > 1:
        v.append("domain_recall10 must be in [0,1]")
    quirks = c.get("provider_quirks") or {}
    if c.get("provider") == "cohere":
        if not (quirks.get("cohere_input_type_index") or "") or not (quirks.get("cohere_input_type_query") or ""):
            v.append("Cohere requires cohere_input_type_index + cohere_input_type_query (rule r4)")
    mn = c.get("model_name") or ""
    if "ada-002" in mn and quirks.get("openai_dimensions") is not None:
        v.append("openai_dimensions param invalid on ada-002 (rule r2)")
    return v


GOOD = {
    "model_name": "text-embedding-3-large",
    "model_version": "2026-04",
    "provider": "openai",
    "corpus_class": "general",
    "dim": 512,
    "metric": "cosine",
    "mteb_retrieval_score": 0.668,
    "domain_recall10": 0.78,
    "provider_quirks": {"openai_dimensions": 512, "max_context_tokens": 8191},
}
BAD = {
    "model_name": "text-embedding-ada-002",
    "model_version": "",
    "provider": "openai",
    "corpus_class": "general",
    "dim": 128,
    "metric": "cosine",
    "mteb_retrieval_score": 0.6,
    "domain_recall10": 0.4,
    "provider_quirks": {"openai_dimensions": 128},
}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("model_version" in x for x in bad)
    assert any("dim" in x for x in bad)
    assert any("ada-002" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-embedding-models.py")
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
