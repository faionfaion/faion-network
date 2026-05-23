#!/usr/bin/env python3
"""validate-cot-basics.py — validate a CoT output sample.

Usage:
    validate-cot-basics.py --sample <path>
    validate-cot-basics.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REASONING_RE = re.compile(r"<reasoning>(.*?)</reasoning>", re.DOTALL)
ANSWER_RE = re.compile(r"<answer>(.*?)</answer>", re.DOTALL)


def validate(text: str) -> list[dict]:
    v: list[dict] = []
    r = REASONING_RE.search(text)
    a = ANSWER_RE.search(text)
    if not r:
        v.append({"rule": "r1", "msg": "missing <reasoning> block"})
    if not a:
        v.append({"rule": "r1", "msg": "missing <answer> block"})
    if r and not r.group(1).strip():
        v.append({"rule": "r1", "msg": "empty <reasoning>"})
    if a and not a.group(1).strip():
        v.append({"rule": "r1", "msg": "empty <answer>"})
    return v


def self_test() -> int:
    good = Path(__file__).parent.parent.joinpath("templates/_smoke-test.txt").read_text(encoding="utf-8")
    assert validate(good) == [], f"smoke must pass: {validate(good)}"
    bad = "Let me think. The answer is 4."
    assert validate(bad), "untagged text must fail"
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sample", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.sample:
        ap.error("--sample required")
        return 2
    text = args.sample.read_text(encoding="utf-8")
    v = validate(text)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
