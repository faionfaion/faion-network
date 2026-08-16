# Value Stream Management

## Summary

**One-sentence:** Maps the end-to-end path from customer request to delivered value and measures flow using Lead Time, Cycle Time, Process Time, %Complete/Accurate, and Throughput.

**One-paragraph:** Maps the end-to-end path from customer request to delivered value and measures flow using Lead Time, Cycle Time, Process Time, %Complete/Accurate, and Throughput. The methodology applies in pm-agile contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-value-stream-management.py` enforces the output contract.

**Ефективно для:**

- Diagnosing where a delivery pipeline stalls (commit → deploy gaps).
- Selecting the single bottleneck step to invest in next quarter.
- Comparing flow efficiency (Process Time / Lead Time) across teams.
- Producing a flow-metrics report for portfolio review.

## Applies If (ALL must hold)

- Team can timestamp each value-stream step (request → analysis → dev → test → deploy → live).
- ≥30 completed items in the last 90 days (statistical floor).
- A single bottleneck can be acted on without org restructure.

## Skip If (ANY kills it)

- <30 completed items in 90 days — sample too small.
- Steps are not timestamped — instrument first.
- Bottleneck requires org-wide restructuring — escalate, do not VSM.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Value-stream step list | ordered list | team |
| Per-item timestamps | CSV/JSON | tool API |
| Throughput target | items/week | PM |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[scrum-ceremonies]] | cadence + ceremony data feeds flow signal |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-flow` | haiku | Mechanical percentile computation. |
| `identify-bottleneck` | sonnet | Judgement: which step holds the longest wait. |
| `draft-report` | sonnet | Narrative around flow metrics. |

## Templates

| File | Purpose |
|------|---------|
| `templates/flow-metrics.py` | Flow-metrics computation from timestamp CSV → JSON report |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[scrum-ceremonies]]
- [[tool-migration-basics]]
- [[earned-value-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/flow-metrics.py`

```python
#!/usr/bin/env python3
"""flow_metrics.py — Lead Time, Cycle Time, and Throughput from transitions CSV.

Input CSV columns required: issue_id, status, ts (ISO 8601 timestamp)
Statuses required: "To Do", "In Progress", "Done"

Usage:
    python3 flow_metrics.py transitions.csv
"""
from __future__ import annotations

import sys
import pandas as pd


def main(path: str) -> int:
    df = pd.read_csv(path, parse_dates=["ts"])

    # Pivot to get first timestamp each issue entered each status
    pivot = df.pivot_table(
        index="issue_id", columns="status", values="ts", aggfunc="min"
    )

    required = {"To Do", "In Progress", "Done"}
    if not required.issubset(pivot.columns):
        missing = required - set(pivot.columns)
        print(f"Missing required statuses: {missing}", file=sys.stderr)
        return 2

    pivot["lead_time_days"] = (
        pivot["Done"] - pivot["To Do"]
    ).dt.total_seconds() / 86400

    pivot["cycle_time_days"] = (
        pivot["Done"] - pivot["In Progress"]
    ).dt.total_seconds() / 86400

    summary = (
        pivot[["lead_time_days", "cycle_time_days"]]
        .dropna()
        .describe(percentiles=[0.5, 0.85, 0.95])
    )
    print("=== Lead Time and Cycle Time ===")
    print(summary.to_string())

    # Throughput per ISO week
    weekly = (
        df[df["status"] == "Done"]
        .set_index("ts")
        .resample("W")["issue_id"]
        .nunique()
    )
    print("\n=== Weekly Throughput (items/week) ===")
    print(weekly.to_string())
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <transitions.csv>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
```
