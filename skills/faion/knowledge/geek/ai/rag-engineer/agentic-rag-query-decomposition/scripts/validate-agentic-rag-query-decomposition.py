#!/usr/bin/env python3
"""Validate decomposer-config artefact.

USAGE:
    validate-agentic-rag-query-decomposition.py <input.json>
    validate-agentic-rag-query-decomposition.py --self-test
    validate-agentic-rag-query-decomposition.py --help

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


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    if c.get("min_sub_queries") != 2:
        v.append("min_sub_queries must be 2 (rule r1)")
    mx = c.get("max_sub_queries")
    if not isinstance(mx, int) or mx < 2 or mx > 4:
        v.append("max_sub_queries must be in [2,4] (rule r1)")
    if not (c.get("planner_model") or "").strip():
        v.append("planner_model required")
    if c.get("parallel") is not True:
        v.append("parallel must be true (rule r2)")
    ct = c.get("confidence_threshold")
    if not isinstance(ct, (int, float)) or ct <= 0 or ct > 1:
        v.append("confidence_threshold must be in (0,1] (rule r3)")
    if c.get("coverage_required") is not True:
        v.append("coverage_required must be true (rule r3)")
    return v


GOOD = {"min_sub_queries": 2, "max_sub_queries": 4, "planner_model": "sonnet", "parallel": True, "confidence_threshold": 0.6, "coverage_required": True}
BAD = {"min_sub_queries": 1, "max_sub_queries": 12, "planner_model": "", "parallel": False, "confidence_threshold": 0.0, "coverage_required": False}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("max_sub_queries" in x for x in bad)
    assert any("parallel" in x for x in bad)
    assert any("coverage_required" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-agentic-rag-query-decomposition.py")
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
