"""
purpose: Reference runner that aggregates yesterday's metrics into triage-report.json.
consumes: eval.json, refusal.jsonl, cost.jsonl from yesterday + 7d baseline
produces: triage-report.json conforming to templates/triage-report.schema.json
depends-on: content/04-procedure.xml
token-budget-impact: CI-only
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def compute_deltas(yest: dict, baseline: dict) -> dict:
    return {
        "eval_score_pp": round((yest["eval_score"] - baseline["eval_score"]) * 100, 2),
        "refusal_rate_pp": round((yest["refusal_rate"] - baseline["refusal_rate"]) * 100, 2),
        "cost_pct": round((yest["cost_per_call"] - baseline["cost_per_call"]) / baseline["cost_per_call"] * 100, 2) if baseline["cost_per_call"] else 0.0,
    }


def pick_top_traces(traces: list[dict]) -> list[dict]:
    failing = [t for t in traces if t.get("passed") is False]
    return [{"id": t["id"], "summary": t.get("summary", ""), "expected": t.get("expected", ""), "got": t.get("got", "")} for t in failing[:3]]


def decide(deltas: dict) -> str:
    if abs(deltas["eval_score_pp"]) >= 5 or abs(deltas["refusal_rate_pp"]) >= 8 or abs(deltas["cost_pct"]) >= 25:
        return "escalate"
    if abs(deltas["eval_score_pp"]) >= 2 or abs(deltas["refusal_rate_pp"]) >= 3 or abs(deltas["cost_pct"]) >= 10:
        return "mitigate"
    return "continue"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--yesterday", type=Path, required=True)
    ap.add_argument("--baseline", type=Path, required=True)
    ap.add_argument("--traces", type=Path, required=True)
    ap.add_argument("--owner", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)

    yest = json.loads(args.yesterday.read_text(encoding="utf-8"))
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    traces = [json.loads(line) for line in args.traces.read_text(encoding="utf-8").splitlines() if line.strip()]
    deltas = compute_deltas(yest, baseline)
    report = {
        "date": str(date.today()),
        "owner": args.owner,
        "deltas": deltas,
        "failing_traces": pick_top_traces(traces),
        "decision": decide(deltas),
        "follow_up": "",
    }
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
