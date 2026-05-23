#!/usr/bin/env python3
"""validate-vector-db-index-tuning.py — validate index-tuning.yaml.

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

REQUIRED = ["workload", "hnsw", "quantization", "sla", "bench", "tuning_history_path"]


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing: {k}")
    hnsw = obj.get("hnsw", {})
    if isinstance(hnsw, dict):
        m = hnsw.get("m", 0)
        if not (16 <= m <= 64):
            errs.append("hnsw.m must be in [16, 64] (r3-workload-driven-m)")
    sla = obj.get("sla", {})
    bench = obj.get("bench", {})
    if isinstance(sla, dict) and isinstance(bench, dict):
        floor = sla.get("recall_floor", 0)
        tuned = bench.get("tuned", {})
        if isinstance(tuned, dict):
            recall = tuned.get("recall", tuned.get("recall_at_10", 0))
            if recall < floor:
                errs.append(f"bench.tuned.recall {recall} < recall_floor {floor} (r5-recall-regression-gate)")
            mem = tuned.get("memory_gb", 0)
            cap = sla.get("memory_cap_gb", float("inf"))
            if mem > cap:
                errs.append(f"bench.tuned.memory_gb {mem} > cap {cap} (fm-05)")
    if "baseline" not in bench:
        errs.append("bench.baseline required (r1-bench-before-tune)")
    if not obj.get("tuning_history_path"):
        errs.append("tuning_history_path required (r4-persist-tuning-record)")
    return errs


FIXTURE_VALID = """
workload: read-heavy
hnsw: {m: 32, ef_construct: 200, ef_search: 128}
quantization: {scheme: scalar}
sla: {recall_floor: 0.90, latency_p95_max_ms: 80, memory_cap_gb: 24}
bench:
  baseline: {recall: 0.84, latency_p95_ms: 38, memory_gb: 41}
  tuned: {recall: 0.93, latency_p95_ms: 62, memory_gb: 18}
tuning_history_path: ops/qdrant/tuning-history.yaml
"""

FIXTURE_INVALID = """
workload: read-heavy
hnsw: {m: 8, ef_construct: 50, ef_search: 8}
quantization: {scheme: binary}
sla: {recall_floor: 0.90, latency_p95_max_ms: 80, memory_cap_gb: 24}
bench:
  tuned: {recall: 0.65, latency_p95_ms: 30, memory_gb: 80}
tuning_history_path: ""
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
    ap = argparse.ArgumentParser(prog="validate-vector-db-index-tuning", description=__doc__,
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
