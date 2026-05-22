#!/usr/bin/env python3
"""validate-latency-vs-quality-decision-grid.py — validate a grid.json.

Usage:
    validate-latency-vs-quality-decision-grid.py --grid <path>
    validate-latency-vs-quality-decision-grid.py --self-test

Inputs: grid.json per templates/grid.schema.json.
Outputs: stdout JSON {ok, violations}
Exit: 0 pass / 1 fail / 2 bad invocation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROW_FIELDS = ["id", "latency_p50_ms", "latency_p95_ms", "quality_floor", "model", "tactic", "cost_per_call_usd", "owner", "last_reviewed"]


def validate(g: dict) -> list[dict]:
    v: list[dict] = []
    for k in ["app", "sites", "rollback_minutes_max"]:
        if k not in g:
            v.append({"rule": "schema", "field": k, "msg": "missing"})
    if v:
        return v
    if g["rollback_minutes_max"] > 5:
        v.append({"rule": "r4", "field": "rollback_minutes_max", "msg": "must be <=5"})
    sites = g.get("sites") or []
    if len(sites) < 3:
        v.append({"rule": "r1", "field": "sites", "msg": "need >=3 sites"})
    seen = set()
    for i, s in enumerate(sites):
        for f in ROW_FIELDS:
            if f not in s or s[f] in (None, ""):
                v.append({"rule": "r3", "field": f"sites[{i}].{f}", "msg": "missing"})
        if s.get("id") in seen:
            v.append({"rule": "r3", "field": f"sites[{i}].id", "msg": f"duplicate id {s['id']}"})
        seen.add(s.get("id"))
        if not (0 <= s.get("quality_floor", -1) <= 1):
            v.append({"rule": "r1", "field": f"sites[{i}].quality_floor", "msg": "quality_floor must be in [0,1]"})
        if s.get("owner", "").strip().lower() in {"team", "us", "tbd"}:
            v.append({"rule": "r3", "field": f"sites[{i}].owner", "msg": "owner must be a named entity"})
    return v


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate(smoke) == [], f"smoke must pass: {validate(smoke)}"
    bad = dict(smoke)
    bad["rollback_minutes_max"] = 30
    assert any(x["rule"] == "r4" for x in validate(bad))
    bad2 = dict(smoke)
    bad2["sites"] = smoke["sites"][:1]
    assert any(x["rule"] == "r1" for x in validate(bad2))
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--grid", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.grid:
        ap.error("--grid required")
        return 2
    data = json.loads(args.grid.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
