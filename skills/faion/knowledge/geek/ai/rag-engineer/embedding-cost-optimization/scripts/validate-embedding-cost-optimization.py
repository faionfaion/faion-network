#!/usr/bin/env python3
"""Validate cost-opt-config artefact.

USAGE:
    validate-embedding-cost-optimization.py <input.json>
    validate-embedding-cost-optimization.py --self-test
    validate-embedding-cost-optimization.py --help

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
    if c.get("dedup_on_ingest") is not True:
        v.append("dedup_on_ingest must be true (rule r1)")
    bs = c.get("batch_size")
    if not isinstance(bs, int) or bs < 32 or bs > 2048:
        v.append("batch_size must be int in [32,2048] (rule r2)")
    if not isinstance(c.get("cache_enabled"), bool):
        v.append("cache_enabled must be boolean")
    md = c.get("matryoshka_dim")
    if not isinstance(md, int) or md < 256 or md > 3072:
        v.append("matryoshka_dim must be int in [256,3072] (rule r4)")
    if not isinstance(c.get("two_stage_retrieval"), bool):
        v.append("two_stage_retrieval must be boolean")
    rt = c.get("recall_tolerance_pp")
    if not isinstance(rt, (int, float)) or rt < 0.0 or rt > 5.0:
        v.append("recall_tolerance_pp must be in [0,5] (rule r4)")
    return v


GOOD = {"dedup_on_ingest": True, "batch_size": 512, "cache_enabled": True, "matryoshka_dim": 512, "two_stage_retrieval": True, "recall_tolerance_pp": 1.0}
BAD = {"dedup_on_ingest": False, "batch_size": 1, "cache_enabled": False, "matryoshka_dim": 64, "two_stage_retrieval": False, "recall_tolerance_pp": 25.0}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("dedup_on_ingest" in x for x in bad)
    assert any("batch_size" in x for x in bad)
    assert any("matryoshka_dim" in x for x in bad)
    assert any("recall_tolerance_pp" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-embedding-cost-optimization.py")
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
