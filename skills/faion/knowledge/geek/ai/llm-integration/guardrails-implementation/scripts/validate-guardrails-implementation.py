#!/usr/bin/env python3
"""Validate output contract for guardrails-implementation.

USAGE:
    validate-guardrails-implementation.py <input.json>   Validate a guardrails-config.json.
    validate-guardrails-implementation.py --self-test    Run built-in fixture.
    validate-guardrails-implementation.py --help         Show this help.

EXIT CODES:
    0 on pass
    1 on schema violation
    2 on usage error

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CHECK_TYPES = {"rule_based", "moderation_api", "llm_check"}
CHECK_ORDER = {"rule_based": 1, "moderation_api": 2, "llm_check": 3}
MIN_RETENTION_DAYS = 90


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    for k in ("version", "input_pipeline", "output_pipeline", "fail_closed", "audit_retention_days"):
        if k not in c:
            v.append(f"missing required field: {k}")
    if not c.get("version"):
        v.append("version is empty (rule r1)")
    ipl = c.get("input_pipeline")
    if not isinstance(ipl, list) or len(ipl) < 1:
        v.append("input_pipeline must be non-empty array (rule r2)")
    seen_orders: list[int] = []
    last_logical = 0
    if isinstance(ipl, list):
        for i, step in enumerate(ipl):
            if not isinstance(step, dict):
                v.append(f"input_pipeline[{i}] must be object")
                continue
            t = step.get("type")
            if t not in CHECK_TYPES:
                v.append(f"input_pipeline[{i}].type invalid: {t!r}")
            o = step.get("order")
            if not isinstance(o, int):
                v.append(f"input_pipeline[{i}].order must be int")
            else:
                seen_orders.append(o)
            if t in CHECK_TYPES:
                logical = CHECK_ORDER[t]
                if logical < last_logical:
                    v.append(f"input_pipeline[{i}] type {t} out of cheap-first order (rule r2)")
                last_logical = max(last_logical, logical)
    if seen_orders and len(seen_orders) != len(set(seen_orders)):
        v.append("input_pipeline order values must be unique")
    op = c.get("output_pipeline") or {}
    if not op.get("validators"):
        v.append("output_pipeline.validators must be non-empty (rule r3)")
    if c.get("fail_closed") is not True:
        v.append("fail_closed must be true (rule r4)")
    ard = c.get("audit_retention_days")
    if isinstance(ard, int) and ard < MIN_RETENTION_DAYS:
        v.append(f"audit_retention_days must be >= {MIN_RETENTION_DAYS} (rule r6)")
    return v


def _self_test() -> int:
    good = {
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
    assert validate(good) == [], f"happy path failed: {validate(good)}"
    bad = {"version": "1", "input_pipeline": [], "fail_closed": False, "audit_retention_days": 30}
    out = validate(bad)
    assert any("input_pipeline" in x for x in out), "must flag empty input_pipeline"
    assert any("fail_closed" in x for x in out), "must flag fail_closed=false"
    assert any("audit_retention_days" in x for x in out), "must flag retention <90"
    # cheap-first check
    bad2 = dict(good)
    bad2["input_pipeline"] = [
        {"type": "llm_check", "order": 1},
        {"type": "rule_based", "order": 2},
    ]
    assert any("cheap-first" in x for x in validate(bad2)), "must flag cheap-first violation"
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-guardrails-implementation.py")
    p.add_argument("path", nargs="?", help="JSON config to validate")
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
