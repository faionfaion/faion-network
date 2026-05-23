#!/usr/bin/env python3
"""validate-cot-techniques.py — validate a cot-config.json.

Usage:
    validate-cot-techniques.py --config <path>
    validate-cot-techniques.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PATTERNS = {"few-shot-cot", "self-consistency", "least-to-most", "tree-of-thoughts"}


def validate(c: dict) -> list[dict]:
    v: list[dict] = []
    if "pattern" not in c or c["pattern"] not in PATTERNS:
        v.append({"rule": "r1", "field": "pattern", "msg": f"must be one of {sorted(PATTERNS)}"})
    cg = c.get("cost_guard") or {}
    if cg.get("max_usd_per_call", 0) <= 0:
        v.append({"rule": "r4", "field": "cost_guard.max_usd_per_call", "msg": "must be > 0"})
    if c.get("pattern") == "self-consistency":
        sc = c.get("self_consistency") or {}
        if not (3 <= sc.get("n_samples", 0) <= 11):
            v.append({"rule": "r5", "field": "self_consistency.n_samples", "msg": "must be in [3,11]"})
        if sc.get("voting_rule") not in {"majority", "median", "llm-judge"}:
            v.append({"rule": "r5", "field": "self_consistency.voting_rule", "msg": "must be majority/median/llm-judge"})
    if c.get("pattern") == "tree-of-thoughts":
        t = c.get("tot") or {}
        if t.get("branches_per_node", 0) > 4:
            v.append({"rule": "r6", "field": "tot.branches_per_node", "msg": "max 4"})
        if t.get("max_depth", 0) > 4:
            v.append({"rule": "r6", "field": "tot.max_depth", "msg": "max 4"})
        if not t.get("value_fn"):
            v.append({"rule": "r6", "field": "tot.value_fn", "msg": "value_fn required"})
    return v


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate(smoke) == [], f"smoke must pass: {validate(smoke)}"
    bad = dict(smoke); bad["self_consistency"] = {"n_samples": 20, "voting_rule": "majority"}
    assert any(x["rule"] == "r5" for x in validate(bad))
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.config:
        ap.error("--config required")
        return 2
    c = json.loads(args.config.read_text(encoding="utf-8"))
    v = validate(c)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
