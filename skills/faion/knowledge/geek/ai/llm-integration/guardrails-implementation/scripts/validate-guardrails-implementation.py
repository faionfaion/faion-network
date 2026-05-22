#!/usr/bin/env python3
"""validate-guardrails-implementation.py — validate a guardrails-config.json.

Usage:
    validate-guardrails-implementation.py --config <path>
    validate-guardrails-implementation.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(c: dict) -> list[dict]:
    v: list[dict] = []
    for k in ["version", "input_pipeline", "output_pipeline", "fail_closed", "audit_retention_days"]:
        if k not in c:
            v.append({"rule": "schema", "field": k, "msg": "missing"})
    if v:
        return v
    if not c.get("fail_closed"):
        v.append({"rule": "r4", "field": "fail_closed", "msg": "must be true"})
    inp = c.get("input_pipeline") or []
    if len(inp) < 1:
        v.append({"rule": "r2", "field": "input_pipeline", "msg": "need >=1 entry"})
    orders = sorted([s.get("order", 0) for s in inp])
    if orders != list(range(1, len(orders) + 1)):
        v.append({"rule": "r2", "field": "input_pipeline.order", "msg": "orders must be 1..N strictly increasing"})
    op = c.get("output_pipeline") or {}
    if "validators" not in op or "filters" not in op:
        v.append({"rule": "r3", "field": "output_pipeline", "msg": "must have validators + filters lists"})
    if c.get("audit_retention_days", 0) < 90:
        v.append({"rule": "r6", "field": "audit_retention_days", "msg": "must be >=90"})
    return v


def _smoke_cfg() -> dict:
    return {
        "version": "1.0.0",
        "input_pipeline": [
            {"type": "rule_based", "order": 1},
            {"type": "moderation_api", "order": 2},
            {"type": "llm_check", "order": 3},
        ],
        "output_pipeline": {"validators": [{"name": "no_pii"}], "filters": [{"name": "strip_links"}]},
        "fail_closed": True,
        "async_fanout": False,
        "audit_retention_days": 90,
    }


def self_test() -> int:
    cfg = _smoke_cfg()
    assert validate(cfg) == [], f"smoke must pass: {validate(cfg)}"
    bad = dict(cfg); bad["fail_closed"] = False
    assert any(x["rule"] == "r4" for x in validate(bad))
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
    data = json.loads(args.config.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
