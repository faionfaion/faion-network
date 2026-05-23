#!/usr/bin/env python3
"""Validate self-correction-config artefact.

USAGE:
    validate-agentic-rag-self-correction.py <input.json>
    validate-agentic-rag-self-correction.py --self-test
    validate-agentic-rag-self-correction.py --help

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
    mc = c.get("max_corrections")
    if not isinstance(mc, int) or mc < 1 or mc > 3:
        v.append("max_corrections must be int in [1,3] (rule r2)")
    g = c.get("generator_model", "")
    ve = c.get("verifier_model", "")
    if not g or not ve:
        v.append("generator_model and verifier_model required")
    elif g == ve:
        v.append("verifier_model must differ from generator_model (rule r1)")
    mu = c.get("max_ungrounded_claims")
    if not isinstance(mu, int) or mu < 0 or mu > 5:
        v.append("max_ungrounded_claims must be int in [0,5] (rule r1)")
    if c.get("audit_trace") is not True:
        v.append("audit_trace must be true (rule r2)")
    return v


GOOD = {"max_corrections": 2, "generator_model": "opus", "verifier_model": "sonnet", "max_ungrounded_claims": 2, "audit_trace": True}
BAD = {"max_corrections": 10, "generator_model": "opus", "verifier_model": "opus", "max_ungrounded_claims": 99, "audit_trace": False}


def _self_test() -> int:
    assert validate(GOOD) == [], f"happy failed: {validate(GOOD)}"
    bad = validate(BAD)
    assert any("max_corrections" in x for x in bad)
    assert any("differ" in x for x in bad)
    assert any("audit_trace" in x for x in bad)
    sys.stdout.write("self-test PASSED\n")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(prog="validate-agentic-rag-self-correction.py")
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
