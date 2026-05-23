#!/usr/bin/env python3
"""Validate chunking-config artefact.

USAGE:
    validate-embedding-chunking-strategies.py <input.json>
    validate-embedding-chunking-strategies.py --self-test
    validate-embedding-chunking-strategies.py --help

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

STRATEGIES = {"fixed_token", "sentence_aware", "recursive", "semantic", "structural", "header_aware", "per_doc_route"}
PROSE_STRATEGIES = {"sentence_aware", "recursive", "semantic"}


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    if c.get("strategy") not in STRATEGIES:
        v.append(f"strategy must be one of {sorted(STRATEGIES)}")
    if c.get("size_unit") != "tokens":
        v.append("size_unit must be 'tokens' (rule r1)")
    cs = c.get("chunk_size")
    if not isinstance(cs, int) or cs < 64 or cs > 4096:
        v.append("chunk_size must be int in [64,4096]")
    ov = c.get("overlap_tokens")
    if not isinstance(ov, int) or ov < 0 or ov > 1024:
        v.append("overlap_tokens must be int in [0,1024]")
    if isinstance(cs, int) and isinstance(ov, int) and cs > 0:
        if c.get("strategy") in PROSE_STRATEGIES and (ov / cs) < 0.10:
            v.append("overlap_tokens/chunk_size must be ≥0.10 on prose strategies (rule r2)")
    mn = c.get("min_tokens")
    if not isinstance(mn, int) or mn < 50:
        v.append("min_tokens must be int ≥50 (rule r5)")
    mx = c.get("max_tokens")
    if not isinstance(mx, int) or mx < 100 or mx > 8192:
        v.append("max_tokens must be int in [100,8192] (rule r5)")
    br = c.get("bench_recall10")
    if not isinstance(br, (int, float)) or br < 0.0 or br > 1.0:
        v.append("bench_recall10 must be in [0,1] (rule r4)")
    return v


GOOD = {"strategy": "recursive", "size_unit": "tokens", "chunk_size": 512, "overlap_tokens": 64, "min_tokens": 60, "max_tokens": 1024, "bench_recall10": 0.78}
BAD = {"strategy": "recursive", "size_unit": "chars", "chunk_size": 512, "overlap_tokens": 0, "min_tokens": 5, "max_tokens": 100000, "bench_recall10": 1.5}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("size_unit" in x for x in bad)
    assert any("overlap_tokens/chunk_size" in x for x in bad)
    assert any("min_tokens" in x for x in bad)
    assert any("max_tokens" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-embedding-chunking-strategies.py")
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
