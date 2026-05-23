#!/usr/bin/env python3
"""validate-rag-pipeline-design.py — validate rag-pipeline.yaml against schema + rules.

Inputs:
    --file PATH    YAML or JSON file to validate
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

REQUIRED = ["tier", "embedding", "vector_db", "chunking", "retrieval", "prompt", "eval_gate", "telemetry"]


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    if obj.get("tier") not in ("naive", "advanced", "modular", "agentic"):
        errs.append("tier must be one of naive|advanced|modular|agentic (r1-tier-selection)")
    retrieval = obj.get("retrieval", {})
    if isinstance(retrieval, dict):
        mode = retrieval.get("mode")
        if mode == "vector":
            errs.append("retrieval.mode='vector' forbidden in production; use 'hybrid' (r2-hybrid-default)")
        elif mode not in ("hybrid", "bm25"):
            errs.append("retrieval.mode must be hybrid|vector|bm25")
    if obj.get("tier") != "naive" and not obj.get("reranker"):
        errs.append("tier!=naive requires reranker block (r4-reranker-after-retrieval)")
    prompt = obj.get("prompt", {})
    if isinstance(prompt, dict) and not prompt.get("citation_required"):
        errs.append("prompt.citation_required must be true (r5-citation-enforcement)")
    eval_gate = obj.get("eval_gate", {})
    if isinstance(eval_gate, dict):
        thr = eval_gate.get("thresholds", {})
        for k in ("faithfulness", "context_recall"):
            if k not in thr:
                errs.append(f"eval_gate.thresholds.{k} missing (r6-eval-gate)")
    chunking = obj.get("chunking", {})
    if isinstance(chunking, dict):
        size = chunking.get("size", 0)
        if size and (size < 100 or size > 1500):
            errs.append("chunking.size out of [100, 1500] band; require explicit override (r3-chunk-default)")
    return errs


FIXTURE_VALID = """
tier: advanced
embedding: {model: voyage-3-large, dim: 1024}
vector_db: {kind: qdrant, connection: {host: x, port: 6333}}
chunking: {strategy: recursive, size: 512, overlap: 50}
retrieval: {mode: hybrid, top_k_first_stage: 20}
reranker: {kind: cohere, model: rerank-v3, top_n: 5}
prompt: {citation_required: true, fallback_phrase: "I don't know"}
eval_gate:
  framework: ragas
  thresholds: {faithfulness: ">= 0.9", context_recall: ">= 0.85"}
telemetry: {log_query_embedding: true, log_retrieved_ids: true, log_scores: true}
"""

FIXTURE_INVALID = """
tier: agentic
embedding: {model: x, dim: 64}
vector_db: {kind: chroma, connection: {}}
chunking: {strategy: fixed, size: 50, overlap: 0}
retrieval: {mode: vector}
prompt: {citation_required: false, fallback_phrase: "x"}
eval_gate: {framework: ragas, thresholds: {}}
telemetry: {log_query_embedding: false, log_retrieved_ids: false, log_scores: false}
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
            raise RuntimeError("pyyaml required for YAML input")
        return yaml.safe_load(raw)
    return json.loads(raw)


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="validate-rag-pipeline-design",
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
