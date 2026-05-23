#!/usr/bin/env python3
"""validate-rag-eval-generation-metrics.

Validates a rag-eval-generation-metrics output JSON against the 02-output-contract schema.

Inputs:  --input PATH    path to output JSON
Outputs: stdout JSON {"ok": bool, "violations": [...]}
Exit:    0 pass, 1 fail
Flags:   --self-test    fixture; --help    print help
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED = {"query_id", "judge_model", "faithfulness", "answer_relevance", "context_relevance"}


def validate(d: dict) -> list[str]:
    v: list[str] = []
    missing = REQUIRED - set(d)
    if missing:
        v.append(f"missing-keys:{sorted(missing)}")
    return v


def _self_test() -> int:
    good = {k: True for k in REQUIRED}
    bad = {}
    return 0 if not validate(good) and validate(bad) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return _self_test()
    if not args.input:
        ap.print_help()
        return 1
    d = json.loads(args.input.read_text(encoding="utf-8"))
    violations = validate(d)
    sys.stdout.write(json.dumps({"ok": not violations, "violations": violations}, indent=2) + "\n")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
