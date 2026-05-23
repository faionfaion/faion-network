#!/usr/bin/env python3
"""validate-reranking.py — validate reranker.yaml.

Inputs:
    --file PATH    YAML or JSON file
    --self-test    Run built-in fixtures
    --help         Show this message

Exit codes:
    0  valid
    1  invalid
    2  usage error
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

REQUIRED = ["provider", "model", "top_n_input", "top_k_output", "latency_budget_ms", "fallback", "eval_evidence"]
PROVIDER_CAPS = {"cohere": 1000, "voyage": 100, "jina": 200, "bge": 500, "flashrank": 1000}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    provider = obj.get("provider")
    top_n = obj.get("top_n_input", 0)
    top_k = obj.get("top_k_output", 0)
    if provider in PROVIDER_CAPS and top_n > PROVIDER_CAPS[provider]:
        errs.append(f"top_n_input {top_n} exceeds {provider} cap {PROVIDER_CAPS[provider]} (r2-top-n-capacity)")
    if top_n < top_k:
        errs.append("top_n_input must be >= top_k_output (no reordering room)")
    if obj.get("latency_budget_ms", 0) < 50:
        errs.append("latency_budget_ms must be >= 50 (r3-latency-budget)")
    fallback = obj.get("fallback", {})
    if isinstance(fallback, dict) and fallback.get("strategy") == "hard-fail":
        errs.append("fallback.strategy must not be hard-fail (r5-fallback-on-outage)")
    ev = obj.get("eval_evidence", {})
    if isinstance(ev, dict):
        if ev.get("sample_size", 0) < 50:
            errs.append("eval_evidence.sample_size >= 50 required (r4-eval-before-adopt)")
        if ev.get("precision_lift", 0) < 0.10:
            errs.append("eval_evidence.precision_lift must be >= 0.10 (r4-eval-before-adopt)")
    return errs


FIXTURE_VALID = """
provider: cohere
model: rerank-multilingual-v3.0
top_n_input: 20
top_k_output: 5
latency_budget_ms: 350
fallback: {strategy: local-bge, model: BAAI/bge-reranker-base}
eval_evidence: {set_path: e.jsonl, sample_size: 84, precision_lift: 0.21}
"""

FIXTURE_INVALID = """
provider: cohere
model: x
top_n_input: 5000
top_k_output: 5
latency_budget_ms: 20
fallback: {strategy: hard-fail}
eval_evidence: {set_path: x, sample_size: 10, precision_lift: 0.02}
"""


def self_test() -> int:
    if yaml is None:
        sys.stderr.write("pyyaml required\n")
        return 2
    if validate(yaml.safe_load(FIXTURE_VALID)):
        sys.stderr.write("valid fixture rejected\n")
        return 1
    errs = validate(yaml.safe_load(FIXTURE_INVALID))
    if not errs:
        sys.stderr.write("invalid fixture accepted\n")
        return 1
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
    ap = argparse.ArgumentParser(
        prog="validate-reranking",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
        obj = load(p)
    except Exception as e:  # noqa: BLE001
        sys.stderr.write(f"parse error: {e}\n")
        return 1
    errs = validate(obj)
    if errs:
        for e in errs:
            sys.stderr.write(f"VIOLATION: {e}\n")
        return 1
    sys.stdout.write("OK\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
