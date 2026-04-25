# Agent Integration — Value Stream Management

## When to use
- Programs where local team optimization no longer produces business throughput gains; bottlenecks live outside the dev team.
- Boards report "green" but customer time-to-value is stuck — VSM exposes the cross-functional friction.
- AI productivity rollouts where dev velocity rose but lead time did not — productivity paradox needs flow visibility.
- DevOps maturity reviews; pair DORA with end-to-end Flow Metrics for a complete picture.
- Multi-team programs (SAFe Value Streams, ARTs) — VSM is foundational.
- Pair with `dora-metrics/`, `predictive-analytics-pm/` (forecasting on flow data), `jira-workflow-management/` + `gitlab-boards/` (data sources), `value-stream-management/` in `project-manager/` (sibling).

## When NOT to use
- Single team, single product, short cycle times — VSM overhead exceeds insight.
- Data quality too poor to trust (status-field abuse, no transitions captured) — fix discipline first.
- Org culture where metrics will be weaponized for performance management — VSM dies on first quarterly review.
- Pure research / discovery work where "value" is exploratory; VSM optimizes flow of known work.
- Where the bottleneck is known and political (e.g., approval committee) and leadership won't intervene — measuring it changes nothing.

## Where it fails / limitations
- Lead-time / cycle-time depend on consistent state transitions; if "In Progress" is abused as a parking lot, metrics lie.
- DORA + Flow are different abstractions; agents that conflate them produce contradictory dashboards (DORA says elite, Flow says blocked).
- Aggregating across heterogeneous teams hides outliers; medians > means; show distributions or you mislead.
- Tools (Plandek, LinearB, Atlassian Atlas, ValueOps) compute differently — switching vendors causes apparent "regressions" from definition changes alone.
- Story points × dollars is not flow efficiency; collapsing them is a common but misleading shortcut.
- Initial VSM workshops produce fishbone-style insights; converting them to durable metrics requires data-engineering work the methodology underestimates.
- Customer-side stages (sales hand-off, onboarding, support) are often outside the team's tooling; partial pipelines yield partial insight.

## Agentic workflow
A `value-stream-mapper` reads issue/MR/incident data and emits a stream definition: stages, owners, entry/exit criteria, current data sources. A `metrics-pipeline` agent extracts events, computes Lead Time, Cycle Time, Process Time, %C/A, Throughput, WIP per stage, and DORA (DF, Lead Time for Changes, CFR, MTTR). A `bottleneck-detector` (Theory-of-Constraints style) flags the largest contributor to lead time and produces a focus action. A `paradox-watcher` correlates AI-tooling rollouts with end-to-end lead-time deltas — flags productivity paradox. Humans approve stream boundaries, ownership claims, and any stage-elimination decision.

### Recommended subagents
- `value-stream-mapper` (sonnet) — synthesize stream from interviews + tool data.
- `metrics-pipeline` (haiku, scheduled) — daily ETL: events → flow + DORA tables.
- `bottleneck-detector` (sonnet) — TOC-style analysis with citations to data spans.
- `paradox-watcher` (sonnet) — correlates tooling/process changes with lead-time deltas.
- `narrative-writer` (sonnet) — translates metrics into stakeholder briefs with caveats.
- `vsm-policy-watcher` (haiku) — alerts on metric definition changes that would break trends.

### Prompt pattern
```
You are bottleneck-detector. Inputs: stage_metrics.csv (stage, count, mean_wait,
mean_process, p95_wait, p95_process, %C/A). Identify the stage that contributes
the largest share of total lead time AND has %C/A < 90 OR queue/process > 4.
Return STRICT JSON: { "primary_bottleneck": "<stage>", "share_of_lead_time":
0.NN, "rationale": "...", "supporting_metrics": {...},
"recommended_focus": ["..."], "non_recommendations": ["..."] }
Rules: do not propose multiple "primary" bottlenecks. Cite numbers, not vibes.
```

```
You are paradox-watcher. Inputs: deployment_frequency.csv, lead_time.csv,
ai_tooling_events.csv (rollout dates). Test if lead-time-for-changes
distribution shifted statistically after each rollout (Mann-Whitney).
Output: { "tool": "...", "rollout_date": "...", "p_value": ...,
"effect_size": ..., "direction": "improved|degraded|no_change",
"caveats": [...] }. Do not infer causation; report associations.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dvc` | Version data snapshots used in VSM analysis | https://dvc.org |
| `duckdb` | Query parquet/CSV without a warehouse | https://duckdb.org |
| `polars` / `pandas` | Tabular wrangling | `pip install polars` |
| `prometheus` + `grafana` | Live flow + DORA dashboards | https://prometheus.io / https://grafana.com |
| `pre-commit` | Block dashboard PRs without metric-definition docs | https://pre-commit.com |
| `mermaid-cli` | Render value-stream diagrams from YAML | `npm i -g @mermaid-js/mermaid-cli` |
| `papermill` | Parameterized notebooks for stage-by-stage analyses | `pip install papermill` |
| `evidently` | Drift on flow metrics over time | https://github.com/evidentlyai/evidently |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Atlassian Atlas / Jira Insights | SaaS | REST | Native flow + roadmaps; opaque computation. |
| LinearB | SaaS | REST | Engineering-metrics with VSM overlay. |
| Plandek | SaaS | REST | Delivery-forecast + flow tooling. |
| Swarmia / Sleuth / Allstacks | SaaS | REST | DORA + flow. |
| Broadcom ValueOps Insights | SaaS | REST | Enterprise VSM, alignment scoring. |
| Tasktop Viz (Planview) | SaaS | REST | Mik Kersten's original product, flow at scale. |
| GitLab Value Stream Analytics | SaaS/OSS | GraphQL | Native VSA on issue/MR events. |
| Azure DevOps Analytics (OData) | SaaS | OData | Powerful query surface for flow. |
| Datadog / Grafana / NewRelic | SaaS/OSS | REST | DORA-from-CI/CD telemetry. |
| Looker / Tableau / Power BI | SaaS | REST | Stakeholder-facing dashboards. |

## Templates & scripts
README is a brief framing piece. Inline below: a script that computes lead time and cycle time from a transitions CSV.

```python
#!/usr/bin/env python3
"""flow_metrics.py — Lead Time, Cycle Time, Throughput from transitions.csv"""
from __future__ import annotations
import sys
import pandas as pd

def main(path: str) -> int:
    df = pd.read_csv(path, parse_dates=["ts"])
    # transitions: issue_id, status, ts
    pivot = df.pivot_table(index="issue_id", columns="status", values="ts", aggfunc="min")
    if not {"To Do", "In Progress", "Done"}.issubset(pivot.columns):
        print("Missing required statuses", file=sys.stderr)
        return 2
    pivot["lead_time_days"] = (pivot["Done"] - pivot["To Do"]).dt.total_seconds() / 86400
    pivot["cycle_time_days"] = (pivot["Done"] - pivot["In Progress"]).dt.total_seconds() / 86400
    summary = pivot[["lead_time_days", "cycle_time_days"]].dropna().describe(percentiles=[.5, .85, .95])
    print(summary.to_string())
    # throughput per ISO week
    weekly = df[df.status == "Done"].set_index("ts").resample("W").issue_id.nunique()
    print("\nWeekly throughput:")
    print(weekly.to_string())
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
```

## Best practices
- Map the value stream end-to-end: customer request → discovery → build → release → operate → outcome. Tool boundaries are not stream boundaries.
- Anchor every metric to a written definition (data source, fields, edges); pin in repo with code review on changes.
- Prefer medians + p85/p95 over means; flow distributions are fat-tailed.
- Pair DORA with Flow Metrics; never report one alone for executives.
- Call out the productivity paradox explicitly: dev velocity ↑ + lead time → → bottleneck moved, not solved.
- Apply Theory of Constraints — focus on the one biggest constraint per quarter; do not multi-task improvements.
- Never use flow metrics for individual performance; aggregate to team or stream.
- Re-baseline only when the stream definition changes; treat tool changes as definition changes.
- Visualize cumulative-flow per stage to see queue accumulation; static averages hide it.
- Wire alerting only on changes large relative to historical noise; avoid alarm fatigue.
- Run quarterly VSM workshops with cross-functional reps; not just engineering.

## AI-agent gotchas
- LLMs invent stages and definitions ("Strategic Lead Time") — pin a glossary file and force lookups.
- Causal claims from observational flow data are dangerous; restrict agents to "associated with".
- Aggregation traps: agents will report mean lead time across heterogeneous teams; require segmentation by team/product.
- DORA "elite" thresholds drift over time and per industry; use cohort-relative comparisons, not absolute labels.
- Productivity-paradox detection requires before/after with rollout dates; without those, agents pattern-match into noise.
- Privacy: per-user metrics are HR-sensitive; refuse to emit; aggregate.
- Definition drift across tools (LinearB vs Plandek vs Atlas) — pin computation logic in code, not vendor.
- Auto-actioning a "bottleneck" finding (re-org, hire, deprioritize) without sponsor sign-off is harmful; agents recommend, humans decide.
- Long-context with raw event streams blows tokens; pre-aggregate at hour/day grain and pass summaries.
- Human-in-the-loop checkpoints (mandatory): stream definition, metric definitions, threshold setting, action approvals.

## References
- Mik Kersten, "Project to Product" (2018) — Flow Framework origin.
- DORA Accelerate (Forsgren, Humble, Kim) — DORA metrics.
- Eli Goldratt, "The Goal" — Theory of Constraints.
- Reinertsen, "The Principles of Product Development Flow".
- SAFe Value Streams reference — https://scaledagileframework.com/value-streams/
- Sibling methodologies: `dora-metrics/`, `predictive-analytics-pm/`, `jira-workflow-management/`, `gitlab-boards/`.
