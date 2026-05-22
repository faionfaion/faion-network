#!/usr/bin/env python3
"""validate-retrieval-drift-alerting-recipe.py — validate drift-alerts.yaml.

Inputs:
    --file PATH    YAML or JSON file to validate
    --self-test    Run against built-in fixtures
    --help         Show this message

Exit codes:
    0  valid
    1  invalid (violations to stderr)
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

REQUIRED = ["baseline", "metrics", "routing", "gate"]
METRIC_NAMES = {
    "query-embedding-kl", "retrieval-set-jaccard",
    "score-histogram-ks", "neighbour-recency",
}


def validate(obj: object) -> list[str]:
    errs: list[str] = []
    if not isinstance(obj, dict):
        return ["root must be an object"]
    for k in REQUIRED:
        if k not in obj:
            errs.append(f"missing required field: {k}")
    baseline = obj.get("baseline", {})
    if isinstance(baseline, dict):
        for k in ("path", "window_days", "captured_at"):
            if k not in baseline:
                errs.append(f"baseline.{k} missing")
        if baseline.get("window_days", 0) < 7:
            errs.append("baseline.window_days must be >=7 (r1-baseline-freshness)")
    metrics = obj.get("metrics", [])
    if not isinstance(metrics, list) or len(metrics) < 4:
        errs.append("metrics must list all 4 metric kinds (r2-four-metric-coverage)")
    else:
        seen = {m.get("name") for m in metrics if isinstance(m, dict)}
        missing = METRIC_NAMES - seen
        if missing:
            errs.append(f"metrics missing required names: {sorted(missing)}")
    routing = obj.get("routing", {})
    if isinstance(routing, dict):
        if routing.get("p1_dual_metric", 0) < 2:
            errs.append("routing.p1_dual_metric must be >=2 (r3-routing-by-severity)")
    gate = obj.get("gate", {})
    if isinstance(gate, dict):
        if not gate.get("enabled"):
            errs.append("gate.enabled must be true (r4-safer-mode-gate)")
        if gate.get("mode") not in ("citations-only", "refuse", "fall-through"):
            errs.append("gate.mode must be one of citations-only|refuse|fall-through")
    return errs


FIXTURE_VALID = """
baseline: {path: "s3://x.parquet", window_days: 14, captured_at: "2026-05-01"}
metrics:
  - {name: query-embedding-kl, kind: distribution, threshold_sigma: 1.0}
  - {name: retrieval-set-jaccard, kind: set, threshold_sigma: 1.0}
  - {name: score-histogram-ks, kind: histogram, threshold_sigma: 1.0}
  - {name: neighbour-recency, kind: recency, threshold_sigma: 1.0}
routing: {p1_dual_metric: 2, p3_single_metric_sustained_min: 60}
gate: {enabled: true, mode: citations-only, flag_name: rag.safer_mode}
"""

FIXTURE_INVALID = """
baseline: {path: "x", window_days: 3, captured_at: "2026-05-01"}
metrics:
  - {name: query-embedding-kl, kind: distribution, threshold_sigma: 1.0}
routing: {p1_dual_metric: 1, p3_single_metric_sustained_min: 60}
gate: {enabled: false, mode: nope, flag_name: x}
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
        prog="validate-retrieval-drift-alerting-recipe",
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
