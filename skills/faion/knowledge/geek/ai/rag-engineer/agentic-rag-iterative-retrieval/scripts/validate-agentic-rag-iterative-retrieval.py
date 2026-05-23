#!/usr/bin/env python3
"""Validate iterative-retriever-config artefact.

USAGE:
    validate-agentic-rag-iterative-retrieval.py <input.json>
    validate-agentic-rag-iterative-retrieval.py --self-test
    validate-agentic-rag-iterative-retrieval.py --help

EXIT CODES:
    0 valid
    1 schema violation
    2 usage / unreadable

NO EXTERNAL DEPS — stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

JUDGE_RE = re.compile(r"^(haiku|sonnet|gpt-5-mini|gemini-flash)")
GEN_RE = re.compile(r"^(opus|sonnet|gpt-5|gemini-pro)")


def validate(c: dict) -> list[str]:
    v: list[str] = []
    if not isinstance(c, dict):
        return ["root must be object"]
    mi = c.get("max_iterations")
    if not isinstance(mi, int) or mi < 1 or mi > 5:
        v.append("max_iterations must be int in [1,5] (rule r1)")
    jm = c.get("judge_model", "")
    gm = c.get("generator_model", "")
    if not JUDGE_RE.match(jm):
        v.append("judge_model must be cheap-class (haiku/sonnet/gpt-5-mini/gemini-flash)")
    if not GEN_RE.match(gm):
        v.append("generator_model must be capable-class (opus/sonnet/gpt-5/gemini-pro)")
    if jm == gm:
        v.append("judge_model must differ from generator_model (rule r2)")
    if c.get("dedup_by_chunk_id") is not True:
        v.append("dedup_by_chunk_id must be true (rule r3)")
    dt = c.get("drift_threshold")
    if not isinstance(dt, (int, float)) or dt < 0.5 or dt > 0.95:
        v.append("drift_threshold must be in [0.5,0.95] (rule r4)")
    return v


GOOD = {
    "max_iterations": 3,
    "judge_model": "haiku",
    "generator_model": "opus",
    "dedup_by_chunk_id": True,
    "drift_threshold": 0.7,
    "sanitise_chunks": True,
}
BAD = {
    "max_iterations": 12,
    "judge_model": "opus",
    "generator_model": "opus",
    "dedup_by_chunk_id": False,
    "drift_threshold": 0.0,
    "sanitise_chunks": False,
}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("max_iterations" in x for x in bad)
    assert any("judge_model" in x for x in bad)
    assert any("differ" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-agentic-rag-iterative-retrieval.py")
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
