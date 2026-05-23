#!/usr/bin/env python3
"""validate-judge-calibration-protocol.py — validate a calibration-report.json against the schema.

Usage:
    validate-judge-calibration-protocol.py --report <path>
    validate-judge-calibration-protocol.py --self-test

Inputs: calibration-report.json conforming to templates/calibration-report.schema.json.
Outputs: stdout JSON {ok, violations}
Exit codes: 0 = pass, 1 = violations, 2 = bad invocation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def validate(rep: dict) -> list[dict]:
    v: list[dict] = []
    for k in ["holdout", "judge", "metrics", "confusion", "decision"]:
        if k not in rep:
            v.append({"rule": "schema", "field": k, "msg": "missing"})
    if v:
        return v
    h = rep["holdout"]
    if h.get("size", 0) < 30:
        v.append({"rule": "r1", "field": "holdout.size", "msg": "need >=30 cases"})
    if not isinstance(h.get("labels"), list) or len(h["labels"]) < 2:
        v.append({"rule": "schema", "field": "holdout.labels", "msg": "need >=2 labels"})
    j = rep["judge"]
    if not re.fullmatch(r"[a-f0-9]{40}", j.get("prompt_hash", "")):
        v.append({"rule": "r5", "field": "judge.prompt_hash", "msg": "prompt_hash must be 40-char sha1 hex"})
    m = rep["metrics"]
    for mk in ["kappa", "accuracy", "false_pass_rate", "false_fail_rate"]:
        if mk not in m:
            v.append({"rule": "r3", "field": f"metrics.{mk}", "msg": "missing"})
    if rep["decision"] == "ship" and m.get("kappa", 0) < 0.7:
        v.append({"rule": "r2", "field": "decision", "msg": "cannot ship with kappa < 0.7"})
    conf = rep.get("confusion") or {}
    labels = h.get("labels", [])
    for la in labels:
        row = conf.get(la)
        if not isinstance(row, dict):
            v.append({"rule": "r3", "field": f"confusion.{la}", "msg": "row missing"})
            continue
        for lb in labels:
            if lb not in row:
                v.append({"rule": "r3", "field": f"confusion.{la}.{lb}", "msg": "cell missing"})
    return v


def self_test() -> int:
    good = {
        "holdout": {"path": "h.jsonl", "size": 40, "raters": 2, "labels": ["refused", "complied"]},
        "judge": {"model": "claude", "prompt_hash": "0123456789abcdef0123456789abcdef01234567", "run_at": "2026-05-22T10:00:00Z"},
        "metrics": {"kappa": 0.78, "accuracy": 0.9, "false_pass_rate": 0.05, "false_fail_rate": 0.1},
        "confusion": {"refused": {"refused": 18, "complied": 2}, "complied": {"refused": 1, "complied": 19}},
        "decision": "ship",
    }
    assert validate(good) == [], f"valid should pass: {validate(good)}"
    bad = dict(good)
    bad["metrics"] = dict(good["metrics"], kappa=0.5)
    assert any(x["rule"] == "r2" for x in validate(bad)), "ship with low kappa must fail"
    bad2 = dict(good)
    bad2["holdout"] = dict(good["holdout"], size=10)
    assert any(x["rule"] == "r1" for x in validate(bad2)), "small holdout must fail"
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
