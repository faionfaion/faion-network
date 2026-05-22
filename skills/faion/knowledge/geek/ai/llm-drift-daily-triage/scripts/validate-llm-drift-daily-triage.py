#!/usr/bin/env python3
"""validate-llm-drift-daily-triage.py — validate a triage-report.json.

Usage:
    validate-llm-drift-daily-triage.py --report <path>
    validate-llm-drift-daily-triage.py --self-test
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

GENERIC_OWNERS = {"team", "us", "tbd", "n/a"}


def validate(rep: dict) -> list[dict]:
    v: list[dict] = []
    for k in ["date", "owner", "deltas", "failing_traces", "decision"]:
        if k not in rep:
            v.append({"rule": "schema", "field": k, "msg": "missing"})
    if v:
        return v
    if rep["owner"].strip().lower() in GENERIC_OWNERS:
        v.append({"rule": "r3", "field": "owner", "msg": "owner must be named, not generic"})
    deltas = rep.get("deltas") or {}
    for k in ["eval_score_pp", "refusal_rate_pp", "cost_pct"]:
        if k not in deltas:
            v.append({"rule": "r2", "field": f"deltas.{k}", "msg": "missing"})
    ft = rep.get("failing_traces", [])
    if len(ft) > 3:
        v.append({"rule": "r2", "field": "failing_traces", "msg": "max 3 traces"})
    for i, t in enumerate(ft):
        for k in ["id", "summary", "expected", "got"]:
            if k not in t:
                v.append({"rule": "r2", "field": f"failing_traces[{i}].{k}", "msg": "missing"})
    if rep["decision"] not in {"continue", "mitigate", "escalate"}:
        v.append({"rule": "r4", "field": "decision", "msg": "decision out of enum"})
    if rep["decision"] == "escalate" and not rep.get("follow_up"):
        v.append({"rule": "r4", "field": "follow_up", "msg": "escalate without follow_up not allowed"})
    return v


def self_test() -> int:
    smoke = json.loads(Path(__file__).parent.parent.joinpath("templates/_smoke-test.json").read_text(encoding="utf-8"))
    for k in list(smoke):
        if k.startswith("_"):
            smoke.pop(k)
    assert validate(smoke) == [], f"smoke must pass: {validate(smoke)}"
    bad = dict(smoke); bad["owner"] = "team"
    assert any(x["rule"] == "r3" for x in validate(bad))
    bad2 = dict(smoke); bad2["decision"] = "escalate"; bad2["follow_up"] = ""
    assert any(x["rule"] == "r4" for x in validate(bad2))
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
    data = json.loads(args.report.read_text(encoding="utf-8"))
    v = validate(data)
    sys.stdout.write(json.dumps({"ok": not v, "violations": v}, indent=2) + "\n")
    return 0 if not v else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
