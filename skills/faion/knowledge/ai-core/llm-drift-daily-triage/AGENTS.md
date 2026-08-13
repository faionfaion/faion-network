# LLM Drift Daily Triage

## Summary

**One-sentence:** Produces a daily 15-minute drift triage — yesterday's eval delta, refusal-rate delta, cost delta, top-3 failing prompts, decision-record (continue / mitigate / escalate).

**One-paragraph:** Model providers ship silent updates; prompt edits land daily; tool descriptions creep. Any of these can move a production behaviour by 5-20 percentage points between yesterday and today. Without a daily 15-minute ritual the signal disappears in the noise and the team finds out from a customer email. This methodology pins a daily report (3 metric deltas + 3 failing-prompt traces + 1 decision) into the on-call rotation; under 15 minutes per day if the report template is filled by the runner.

**Ефективно для:** customer-facing AI products, regulated pipelines (finance, health), agents with paid downstream effects, model upgrades pre-rollout.

## Applies If (ALL must hold)

- A production LLM call path has run for ≥7 days (enough history for a delta).
- A daily eval pulse exists (cron, GitHub Action, etc.) producing per-day scores.
- An on-call (or single owner) reviews the report.
- A decision channel exists (Slack, ticket, alert) where the day's decision is recorded.

## Skip If (ANY kills it)

- No production traffic — drift is hypothetical.
- No eval set — there is no signal to triage; bootstrap the eval first.
- Single-shot pipeline, never updated — drift surface is empty.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Daily eval-run summary | JSON | eval runner artifact |
| Refusal-rate log | JSONL | application telemetry |
| Cost-per-call log | JSONL | billing webhook / cost dashboard |
| On-call rotation | calendar | PagerDuty / OpsGenie |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[jailbreak-eval-suite-bootstrap]]` | Suite produces the eval-delta input. |
| `[[ai-cost-attribution-schema]]` | Cost log uses the attribution schema. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: 15-min cap, 3-delta + 3-trace report, named owner, escalation path, weekly trend, no-skip | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for triage-report.json | ~600 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: skipped-day, eyeball-only, no-escalation, single-metric-tunnel, retro-edit | ~600 |
| `content/04-procedure.xml` | medium | 6-step procedure: pull metrics → compute deltas → load failing traces → decide → log → schedule follow-up | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "is the absolute eval delta > 2pp OR refusal-rate delta > 3pp OR cost delta > 10%?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Pull metrics & compute deltas | haiku | Deterministic numerical. |
| Summarise top-3 failing traces | sonnet | Bounded summarisation. |
| Recommend decision | opus | Multi-axis reasoning. |
| File ticket / page on-call | haiku | Mechanical channel write. |

## Templates

| File | Purpose |
|---|---|
| `templates/triage-report.schema.json` | JSON Schema for the daily report. |
| `templates/triage-report.md` | Markdown skeleton (3 deltas + 3 traces + decision). |
| `templates/runner.py` | Reference runner that produces triage-report.json from telemetry sources. |
| `templates/_smoke-test.json` | Minimum-viable triage report. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-llm-drift-daily-triage.py` | Validates triage-report.json schema + asserts owner + decision present. | Pre-commit on report PR; CI before posting to Slack. |

## Related

- parent skill: `geek/ai/`
- `[[ai-cost-attribution-schema]]`
- `[[jailbreak-eval-suite-bootstrap]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` decides the day's action: small deltas → continue (log only); medium deltas → mitigate (revert last change, page owner); large deltas → escalate (incident + page on-call). Thresholds are configurable per call site.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/triage-report.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/llm-drift-daily-triage",
  "_purpose": "Schema for the daily drift triage report.",
  "_consumes": "operator-filled or runner-emitted triage-report.json",
  "_produces": "validation verdict",
  "_depends_on": "content/02-output-contract.xml",
  "_token_budget_impact": "validator only",
  "type": "object",
  "required": [
    "date",
    "owner",
    "deltas",
    "failing_traces",
    "decision"
  ],
  "properties": {
    "date": {
      "type": "string"
    },
    "owner": {
      "type": "string"
    },
    "deltas": {
      "type": "object",
      "required": [
        "eval_score_pp",
        "refusal_rate_pp",
        "cost_pct"
      ],
      "properties": {
        "eval_score_pp": {
          "type": "number"
        },
        "refusal_rate_pp": {
          "type": "number"
        },
        "cost_pct": {
          "type": "number"
        }
      }
    },
    "failing_traces": {
      "type": "array",
      "maxItems": 3,
      "items": {
        "type": "object",
        "required": [
          "id",
          "summary",
          "expected",
          "got"
        ]
      }
    },
    "decision": {
      "enum": [
        "continue",
        "mitigate",
        "escalate"
      ]
    },
    "follow_up": {
      "type": "string"
    }
  }
}
```

### `templates/runner.py`

```python
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
```

### `templates/_smoke-test.json`

```json
{
  "_purpose": "Minimum viable triage report that passes the validator.",
  "_consumes": "validate-llm-drift-daily-triage.py",
  "_produces": "ok verdict",
  "_depends_on": "templates/triage-report.schema.json",
  "_token_budget_impact": "docs-only",
  "date": "2026-05-22",
  "owner": "alex.engineer",
  "deltas": {
    "eval_score_pp": -0.5,
    "refusal_rate_pp": 0.2,
    "cost_pct": 1.0
  },
  "failing_traces": [],
  "decision": "continue",
  "follow_up": ""
}
```
