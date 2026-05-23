#!/usr/bin/env python3
"""validate-rag-eval-ab-testing.

Validates a RAG A/B report JSON against the 02-output-contract schema.

Inputs:  --input PATH    report JSON path
Outputs: stdout JSON {"ok": bool, "violations": [...]}
Exit:    0 pass, 1 fail
Flags:   --self-test    fixture; --help    print help
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RECS = {"promote-b", "keep-a", "run-more"}


def validate(d: dict) -> list[str]:
    v: list[str] = []
    for k in ("config_a", "config_b", "n_questions", "per_question", "aggregate", "recommendation"):
        if k not in d:
            v.append(f"missing:{k}")
    if d.get("n_questions", 0) < 20:
        v.append(f"n_questions-too-small:{d.get('n_questions')}")
    if d.get("recommendation") not in RECS:
        v.append(f"bad-recommendation:{d.get('recommendation')}")
    a = d.get("aggregate", {})
    for k in ("metric", "a_mean", "b_mean", "p_value", "a_latency_p95_ms", "b_latency_p95_ms"):
        if k not in a:
            v.append(f"aggregate-missing:{k}")
    return v


def _self_test() -> int:
    good = {"config_a": "a", "config_b": "b", "n_questions": 20, "per_question": [],
            "aggregate": {"metric": "faithfulness", "a_mean": 0.8, "b_mean": 0.85, "p_value": 0.02, "a_latency_p95_ms": 1000, "b_latency_p95_ms": 1100},
            "recommendation": "promote-b"}
    bad = {"config_a": "a", "n_questions": 5}
    return 0 if not validate(good) and validate(bad) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if not args.input:
        ap.print_help()
        return 1
    d = json.loads(args.input.read_text(encoding="utf-8"))
    violations = validate(d)
    sys.stdout.write(json.dumps({"ok": not violations, "violations": violations}, indent=2) + "\n")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
