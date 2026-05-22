#!/usr/bin/env python3
"""validate-hybrid-search-basics.

Validates a hybrid-search YAML config against the 02-output-contract.xml schema.

Inputs:  --input PATH    path to a YAML config
Outputs: stdout JSON {"ok": bool, "violations": [...]}
Exit:    0 on pass, 1 on fail
Flags:   --self-test    run against a built-in fixture
         --help          print this help
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(json.dumps({"ok": False, "violations": ["pyyaml-not-installed"]}))
    sys.exit(1)

FUSIONS = {"rrf", "linear"}
SPARSE_BACKENDS = {"bm25", "splade", "tantivy"}
TIE_BREAKS = {"dense_rank", "sparse_rank", "doc_id"}


def validate(c: dict) -> list[str]:
    v: list[str] = []
    for key in ("fusion", "dense", "sparse", "k", "tie_break", "eval"):
        if key not in c:
            v.append(f"missing:{key}")
    if c.get("fusion") not in FUSIONS:
        v.append(f"bad-fusion:{c.get('fusion')}")
    if c.get("fusion") == "linear" and "alpha" not in c:
        v.append("linear-missing-alpha")
    if "alpha" in c and not (0 <= c["alpha"] <= 1):
        v.append(f"bad-alpha:{c['alpha']}")
    d = c.get("dense", {})
    if not isinstance(d, dict) or "index" not in d or "model" not in d:
        v.append("dense-incomplete")
    s = c.get("sparse", {})
    if not isinstance(s, dict) or s.get("backend") not in SPARSE_BACKENDS:
        v.append("sparse-bad")
    if c.get("tie_break") not in TIE_BREAKS:
        v.append(f"bad-tie-break:{c.get('tie_break')}")
    e = c.get("eval", {})
    if not isinstance(e, dict) or any(k_ not in e for k_ in ("dataset", "metric", "score")):
        v.append("eval-incomplete")
    return v


def _self_test() -> int:
    good = {"fusion": "rrf", "dense": {"index": "x", "model": "m"}, "sparse": {"backend": "bm25"}, "k": 10, "tie_break": "dense_rank", "eval": {"dataset": "d", "metric": "ndcg@10", "score": 0.7}}
    bad = {"fusion": "linear", "dense": {"index": "x"}, "sparse": {}, "k": 10}
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
    c = yaml.safe_load(args.input.read_text(encoding="utf-8"))
    violations = validate(c)
    sys.stdout.write(json.dumps({"ok": not violations, "violations": violations}, indent=2) + "\n")
    return 0 if not violations else 1


if __name__ == "__main__":
    raise SystemExit(main())
