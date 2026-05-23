#!/usr/bin/env python3
"""validate-guardrails-basics.py — validate a guardrails-spec.json.

Usage:
    validate-guardrails-basics.py --spec <path>
    validate-guardrails-basics.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(s: dict) -> list[dict]:
    v: list[dict] = []
    layers = s.get("layers") or []
    if len(layers) < 4:
        v.append({"rule": "r1", "field": "layers", "msg": f"need >=4 layers, got {len(layers)}"})
    types_present = [l.get("type") for l in layers]
    if "llm_classifier" in types_present:
        idx = next(l for l in layers if l.get("type") == "llm_classifier")
        max_order = max(l.get("order", 0) for l in layers)
        if idx.get("order") != max_order:
            v.append({"rule": "r4", "field": "layers", "msg": "llm_classifier must have highest order"})
    if not s.get("fail_closed"):
        v.append({"rule": "r5", "field": "fail_closed", "msg": "must be true"})
    if not (50 <= s.get("latency_budget_ms", 0) <= 2000):
        v.append({"rule": "r2", "field": "latency_budget_ms", "msg": "must be in [50, 2000]"})
    return v


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate(smoke) == [], f"smoke must pass: {validate(smoke)}"
    bad = dict(smoke); bad["fail_closed"] = False
    assert any(x["rule"] == "r5" for x in validate(bad))
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.spec:
        ap.error("--spec required")
        return 2
    data = json.loads(args.spec.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
