#!/usr/bin/env python3
"""validate-jailbreak-eval-suite-bootstrap.py — validate suite-config.yaml + eval-cases.jsonl.

Usage:
    validate-jailbreak-eval-suite-bootstrap.py --config <suite-config.yaml> --cases <cases.jsonl>
    validate-jailbreak-eval-suite-bootstrap.py --self-test

Inputs: YAML config + JSONL cases.
Outputs: stdout JSON {ok, violations}
Exit codes: 0 = pass, 1 = violations, 2 = bad invocation.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise SystemExit("pyyaml required: pip install pyyaml")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate(config: dict, cases: list[dict]) -> list[dict]:
    v: list[dict] = []
    cats = config.get("categories") or []
    if len(cats) < 10:
        v.append({"rule": "r1", "field": "categories", "msg": f"need >=10 categories, got {len(cats)}"})
    thr = config.get("thresholds") or {}
    if "global" in thr:
        v.append({"rule": "r5", "field": "thresholds.global", "msg": "no global threshold; use per-category"})
    missing = [c for c in cats if c not in thr]
    if missing:
        v.append({"rule": "r5", "field": "thresholds", "msg": f"missing thresholds for {missing}"})
    judge = config.get("judge") or {}
    if not judge.get("calibration"):
        v.append({"rule": "r4", "field": "judge.calibration", "msg": "calibration path required"})
    if judge.get("kappa_min", 0) < 0.7:
        v.append({"rule": "r4", "field": "judge.kappa_min", "msg": "kappa_min must be >=0.7"})
    ci = config.get("ci") or {}
    if not ci.get("trigger_paths"):
        v.append({"rule": "r6", "field": "ci.trigger_paths", "msg": "trigger_paths required"})
    if ci.get("regression_pp", 99) > 1.0:
        v.append({"rule": "r6", "field": "ci.regression_pp", "msg": "regression_pp should be <=1.0"})

    counts = Counter()
    for i, c in enumerate(cases):
        for k in ["id", "category", "prompt", "judge_kind", "citation", "expected"]:
            if k not in c:
                v.append({"rule": "r3", "field": f"case[{i}].{k}", "msg": "missing required case field"})
        if c.get("judge_kind") not in {"regex", "llm"}:
            v.append({"rule": "r3", "field": f"case[{i}].judge_kind", "msg": "judge_kind must be regex or llm"})
        if c.get("expected") not in {"refused", "complied"}:
            v.append({"rule": "r3", "field": f"case[{i}].expected", "msg": "expected must be refused/complied"})
        counts[c.get("category")] += 1
    for cat in cats:
        if counts.get(cat, 0) < 5:
            v.append({"rule": "r2", "field": f"cases.{cat}", "msg": f"need >=5 cases per category, got {counts.get(cat, 0)}"})
    return v


def self_test() -> int:
    cfg = {
        "categories": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
        "thresholds": {c: 0.95 for c in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]},
        "judge": {"calibration": "x.jsonl", "kappa_min": 0.75},
        "ci": {"trigger_paths": ["x"], "regression_pp": 1.0},
    }
    cases = []
    for cat in cfg["categories"]:
        for n in range(5):
            cases.append({"id": f"{cat}-{n}", "category": cat, "prompt": "p", "judge_kind": "regex", "judge_args": {"refusal_pattern": "x"}, "citation": "s", "expected": "refused"})
    assert validate(cfg, cases) == [], f"valid bundle should pass: {validate(cfg, cases)}"
    bad = dict(cfg)
    bad["categories"] = ["a"]
    assert any(x["rule"] == "r1" for x in validate(bad, cases)), "should flag <10 categories"
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path)
    ap.add_argument("--cases", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.config or not args.cases:
        ap.error("--config and --cases required")
        return 2
    cfg = load_yaml(args.config)
    cases = [json.loads(line) for line in args.cases.read_text(encoding="utf-8").splitlines() if line.strip() and "_purpose" not in line]
    v = validate(cfg, cases)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
