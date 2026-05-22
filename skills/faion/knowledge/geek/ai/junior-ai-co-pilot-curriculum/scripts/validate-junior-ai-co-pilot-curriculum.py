#!/usr/bin/env python3
"""validate-junior-ai-co-pilot-curriculum.py — validate a curriculum.json.

Usage:
    validate-junior-ai-co-pilot-curriculum.py --curriculum <path>
    validate-junior-ai-co-pilot-curriculum.py --self-test

Inputs: curriculum.json per templates/curriculum.schema.json.
Outputs: stdout JSON {ok, violations}
Exit codes: 0 pass / 1 fail / 2 bad invocation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_MODULES = {"prompt anatomy", "hallucination check", "scoped edits", "test-first ai", "security boundaries", "mentor review"}


def validate(cur: dict) -> list[dict]:
    v: list[dict] = []
    for k in ["junior_name", "mentor_name", "tool", "weeks", "modules", "rubric"]:
        if k not in cur:
            v.append({"rule": "schema", "field": k, "msg": "missing"})
    if v:
        return v
    if not (4 <= cur["weeks"] <= 8):
        v.append({"rule": "r1", "field": "weeks", "msg": "weeks must be in [4, 8]"})
    mods = cur.get("modules") or []
    if len(mods) < 6:
        v.append({"rule": "r2", "field": "modules", "msg": "need >=6 modules"})
    titles = {m.get("title", "").strip().lower() for m in mods}
    missing = REQUIRED_MODULES - titles
    if missing:
        v.append({"rule": "r2", "field": "modules.titles", "msg": f"missing required modules: {sorted(missing)}"})
    for i, m in enumerate(mods):
        if not m.get("reflection_required", False):
            v.append({"rule": "r3", "field": f"modules[{i}].reflection_required", "msg": "must be true"})
    rub = cur.get("rubric") or []
    if len(rub) < 10:
        v.append({"rule": "r5", "field": "rubric", "msg": "need >=10 rubric items"})
    for i, r in enumerate(rub):
        for k in ["id", "statement", "evidence"]:
            if not r.get(k):
                v.append({"rule": "r5", "field": f"rubric[{i}].{k}", "msg": "missing"})
    return v


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    smoke.pop("_purpose", None); smoke.pop("_consumes", None); smoke.pop("_produces", None); smoke.pop("_depends_on", None); smoke.pop("_token_budget_impact", None)
    assert validate(smoke) == [], f"smoke must pass: {validate(smoke)}"
    bad = dict(smoke)
    bad["weeks"] = 2
    assert any(x["rule"] == "r1" for x in validate(bad)), "should flag short weeks"
    bad2 = dict(smoke)
    bad2["rubric"] = []
    assert any(x["rule"] == "r5" for x in validate(bad2)), "should flag empty rubric"
    sys.stdout.write("self-test: OK\n")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--curriculum", type=Path)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.curriculum:
        ap.error("--curriculum required")
        return 2
    data = json.loads(args.curriculum.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
