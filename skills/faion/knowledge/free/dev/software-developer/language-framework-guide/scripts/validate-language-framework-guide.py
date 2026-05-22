#!/usr/bin/env python3
"""validate-language-framework-guide.py — validate a stack-recommendation report.

Usage:
    validate-language-framework-guide.py --report rec.json
    validate-language-framework-guide.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def validate(rep: dict) -> list[dict]:
    v: list[dict] = []
    p = rep.get("primary", {})
    if not all(k in p for k in ("language", "framework", "rationale")):
        v.append({"rule": "rule:r5", "message": "primary missing language/framework/rationale"})
    elif len(p.get("rationale", "")) < 30:
        v.append({"rule": "rule:r5", "message": "rationale too short (<30 chars)"})
    alts = rep.get("alternatives", [])
    if len(alts) != 2:
        v.append({"rule": "rule:r5", "message": f"alternatives count {len(alts)} (must be 2)"})
    for i, a in enumerate(alts):
        if not all(k in a for k in ("language", "framework", "tradeoff")):
            v.append({"rule": "rule:r5", "message": f"alternative {i} missing language/framework/tradeoff"})
        elif len(a.get("tradeoff", "")) < 20:
            v.append({"rule": "rule:r5", "message": f"alternative {i} tradeoff too short"})
    adr = rep.get("adrStub", {})
    for k in ("status", "context", "decision", "alternatives", "consequences"):
        if k not in adr:
            v.append({"rule": "rule:r6", "message": f"adrStub missing {k}"})
    return v


def self_test() -> int:
    good = {
        "primary": {"language": "python", "framework": "fastapi",
                    "rationale": "Async API for a solo dev, mature ecosystem, broad LLM coverage."},
        "alternatives": [
            {"language": "typescript", "framework": "next.js", "tradeoff": "Pays full-stack tax for API-only need."},
            {"language": "go", "framework": "gin", "tradeoff": "Higher RPS, more ceremony."},
        ],
        "adrStub": {"status": "proposed", "context": "Solo founder, 12-month API project for marketing dashboards.",
                    "decision": "Adopt Python + FastAPI.", "alternatives": "Next.js, Go+Gin.",
                    "consequences": "Hiring constrained to Python; OK for solo."},
    }
    assert not validate(good), f"good must pass: {validate(good)}"
    bad = {"primary": {"language": "rust"}}
    v = validate(bad)
    assert v, f"bad must fail: {v}"
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.report:
        ap.error("--report required")
        return 2
    rep = json.loads(args.report.read_text(encoding="utf-8"))
    v = validate(rep)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
