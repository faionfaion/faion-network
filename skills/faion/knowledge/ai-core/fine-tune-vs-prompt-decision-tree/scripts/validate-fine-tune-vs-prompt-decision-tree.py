#!/usr/bin/env python3
"""validate-fine-tune-vs-prompt-decision-tree.py — validate a 4-axis decision artefact.

Usage:
    validate-fine-tune-vs-prompt-decision-tree.py --record file.json
    validate-fine-tune-vs-prompt-decision-tree.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ALTS = {"prompt-improve", "rag", "routing", "distillation"}


def validate(d: dict) -> list[dict]:
    v: list[dict] = []
    for k in ("workload", "owner", "created_at", "axes", "alternatives_tried", "recommendation", "revisit_triggers"):
        if k not in d:
            v.append({"rule": "schema", "message": f"missing: {k}"})
    if v:
        return v
    if d["owner"] in ("team", "everyone", "TBD", ""):
        v.append({"rule": "rule:r5", "message": "owner not named"})
    for axis in ("quality", "cost", "latency", "maintenance"):
        if axis not in d["axes"]:
            v.append({"rule": "rule:r1", "message": f"axis missing: {axis}"})
            continue
        a = d["axes"][axis]
        if not (1 <= a.get("score", 0) <= 5) or len(a.get("note", "")) < 5:
            v.append({"rule": "rule:r1", "message": f"axis {axis} malformed"})
    alts = {a["alt"]: a for a in d["alternatives_tried"]}
    if not ALTS.issubset(alts):
        v.append({"rule": "rule:r2", "message": f"missing alternatives: {sorted(ALTS - alts.keys())}"})
    if len(d["revisit_triggers"]) < 2 or any(len(t) < 10 for t in d["revisit_triggers"]):
        v.append({"rule": "rule:r4", "message": "need ≥2 revisit_triggers ≥10 chars each"})
    if d["recommendation"] == "fine-tune":
        below = sum(1 for x in d["axes"].values() if x.get("score", 5) <= 2)
        if below < 2:
            v.append({"rule": "rule:r3", "message": "FT needs ≥2 axes scored ≤2"})
        tried_alts = [a for a in d["alternatives_tried"] if a["status"] == "tried"]
        if len(tried_alts) < 3:
            v.append({"rule": "rule:r2", "message": "FT requires ≥3 alternatives tried"})
    return v


def self_test() -> int:
    good = {
        "workload": "chat-classifier", "owner": "alice@example.com",
        "created_at": "2026-05-22",
        "axes": {
            "quality":     {"score": 3, "note": "F1 0.79"},
            "cost":        {"score": 2, "note": "1.4c/req"},
            "latency":     {"score": 4, "note": "p95 320ms"},
            "maintenance": {"score": 4, "note": "1 prompt"},
        },
        "alternatives_tried": [
            {"alt": "prompt-improve", "lift": 0.02, "status": "tried"},
            {"alt": "rag", "lift": 0.0, "status": "tried"},
            {"alt": "routing", "lift": 0.04, "status": "tried"},
            {"alt": "distillation", "lift": None, "status": "untried"},
        ],
        "recommendation": "routing",
        "revisit_triggers": ["volume crosses 200k req/day", "F1 drops below 0.78 for 3 days"],
    }
    assert validate(good) == [], validate(good)
    bad = dict(good, owner="team", revisit_triggers=[])
    out = validate(bad)
    assert any(x["rule"] == "rule:r5" for x in out), out
    assert any(x["rule"] == "rule:r4" for x in out), out
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
