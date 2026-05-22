#!/usr/bin/env python3
"""validate-finetune-cost-vs-prompt-decision.py — validate a FT-vs-prompt decision record.

Usage:
    validate-finetune-cost-vs-prompt-decision.py --record file.json
    validate-finetune-cost-vs-prompt-decision.py --self-test

Exit codes: 0=pass, 1=fail, 2=bad invocation.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path


def validate(d: dict) -> list[dict]:
    v: list[dict] = []
    req = ["workload", "owner", "created_at", "recheck_at", "lift_bar", "baseline",
           "candidate", "break_even_months", "strong_signals", "recommendation"]
    for k in req:
        if k not in d:
            v.append({"rule": "schema", "message": f"missing: {k}"})
    if v:
        return v
    if d["owner"] in ("team", "everyone", "TBD", ""):
        v.append({"rule": "rule:r4", "message": f"owner must be named, got {d['owner']!r}"})
    try:
        c = date.fromisoformat(d["created_at"])
        r = date.fromisoformat(d["recheck_at"])
        if (r - c).days > 200:
            v.append({"rule": "rule:r5", "message": f"recheck_at {(r-c).days}d after created_at; max 180"})
    except (ValueError, KeyError) as e:
        v.append({"rule": "schema", "message": f"date parse error: {e}"})
    if not (0.001 <= d["lift_bar"] <= 0.5):
        v.append({"rule": "rule:r1", "message": f"lift_bar {d['lift_bar']} outside [0.001,0.5]"})
    if d["recommendation"] == "fine-tune":
        if not d.get("strong_signals") or len(d["strong_signals"]) < 2:
            v.append({"rule": "rule:r3", "message": "fine-tune needs ≥2 strong_signals"})
        if d.get("break_even_months") is None:
            v.append({"rule": "rule:r2", "message": "fine-tune needs break_even_months computed"})
        elif d["break_even_months"] > 12:
            v.append({"rule": "rule:r2", "message": f"break_even_months {d['break_even_months']} > 12"})
    return v


def self_test() -> int:
    good = {
        "workload": "support-classifier",
        "owner": "alice.chen@example.com",
        "created_at": "2026-05-22",
        "recheck_at": "2026-11-22",
        "lift_bar": 0.05,
        "baseline": {"score": 0.78, "cost_per_k_tokens": 3.0, "daily_volume": 50000},
        "candidate": {"training_cost": 800, "hosting_cost_per_k_tokens": 0.5, "training_examples": 6500},
        "break_even_months": 2.1,
        "strong_signals": ["data-volume-5k+", "cost-amortises-12mo", "latency-critical"],
        "recommendation": "fine-tune",
    }
    assert validate(good) == [], validate(good)
    bad = dict(good, owner="team", recheck_at="2030-01-01", strong_signals=["data-volume-5k+"],
               break_even_months=None)
    out = validate(bad)
    assert any(x["rule"] == "rule:r4" for x in out), out
    assert any(x["rule"] == "rule:r5" for x in out), out
    assert any(x["rule"] == "rule:r3" for x in out), out
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--record", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.record:
        ap.error("--record required")
        return 2
    out = validate(json.loads(args.record.read_text(encoding="utf-8")))
    sys.stdout.write(json.dumps({"ok": not out, "violations": out}, indent=2) + "\n")
    return 0 if not out else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
