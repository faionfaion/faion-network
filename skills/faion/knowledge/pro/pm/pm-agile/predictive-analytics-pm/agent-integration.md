# Agent Integration — Predictive Analytics in PM

## When to use
- Backlogs and historical project data large enough (≥ 200 closed items, ≥ 6 months) for forecasting to beat naive baselines.
- Schedule risk early-warning: detect "this sprint will miss" 3–5 days before the burn-down does.
- Budget overrun detection: compare run-rate trends with planned spend, surface variances early.
- Resource utilization optimization across multi-team programs (skill matching, contention).
- Risk pattern mining: find leading indicators (epic age, comment sentiment, churn) of late delivery.
- Material/vendor cost forecasting where commodity prices drive a meaningful share of project cost.
- Pair with `value-stream-management/` (DORA + Flow Metrics input data), `jira-workflow-management/` (data source), `dora-metrics/`.

## When NOT to use
- Small teams or new projects without historical data — predictive models will overfit / underperform expert estimation.
- Hand-managed spreadsheets without consistent fields — data quality kills the signal before any model runs.
- Decision-making that needs explainability you cannot provide (regulated procurement, public-sector audits) — black-box ML blocked.
- "AI dashboards" stakeholders cannot read — predictive output without a human translator becomes shelf-ware.
- One-off projects without comparable history to learn from.
- When the underlying issue is organizational (priorities flip weekly), no model fixes that — leadership intervention needed.

## Where it fails / limitations
- Garbage-in: status-field discipline is the bottleneck. If "In Progress" actually means "abandoned", every metric lies.
- Concept drift: team composition changes, process changes, scope changes — yesterday's velocity model is stale within months.
- Survivorship bias: training on completed projects ignores the cancelled / silent-fail projects that carry the lessons.
- Calibration: probability outputs ("70% likely to slip") need calibration; uncalibrated agents emit overconfident forecasts.
- Causal vs. correlational confusion — the model says "long descriptions correlate with overrun", PMs ban long descriptions, the underlying cause stays.
- LLM-only forecasting (no numeric model) is unreliable beyond simple regression; use proper estimators.
- Privacy/HR risk: per-person productivity metrics from issue data attract regulatory scrutiny; aggregate at team level.

## Agentic workflow
A `data-extractor` pulls issue/cycle data from Jira/Linear/GitHub/GitLab into a tidy parquet table (one row per issue-state-transition). A `feature-builder` derives lead-time, cycle-time, age, churn, comment-count, blocker-age, skill match. A classical-ML model (gradient boosting / Cox / hazard) produces forecasts; an `analyst-agent` (LLM) writes a plain-language brief explaining drivers and recommended actions, but never the predictions themselves. A `forecast-monitor` tracks calibration and decision impact; flags drift. Humans approve any action that re-allocates resources, pulls scope, or triggers escalation.

### Recommended subagents
- `data-extractor` (haiku) — paginated REST/GraphQL pulls, schema validation, snapshot to parquet.
- `feature-builder` (haiku) — deterministic transformations; no inference.
- `forecast-runner` (sonnet, calls model API) — invokes the trained model, attaches confidence intervals.
- `analyst-agent` (sonnet) — translates forecasts into stakeholder briefs with caveats.
- `forecast-monitor` (haiku, scheduled) — calibration plots, drift alarms, retraining trigger.
- `policy-watch-agent` (haiku) — watches PMI / org policy on AI-driven decisions; blocks releases that violate.

### Prompt pattern
```
You are analyst-agent. Inputs: forecast.json (point estimates + 80% CIs +
top SHAP features), program_context.md. Produce a stakeholder brief in 3
sections: (1) headline forecast in plain language, (2) the 3 most important
drivers with one-sentence explanations, (3) recommended human decisions.
Rules: never assert causation; say "associated with"; no numeric precision
beyond the model's CI; flag low confidence (CI width > 30% of point) as
"low confidence — treat as direction only".
```

```
You are data-extractor. Pull issues from Jira project KEY, time range
[start, end], with fields: status_history, assignee, story_points,
created, resolved, components, labels. Validate against schema X. Write
parquet to ./data/raw/{KEY}_{date}.parquet. Refuse if rate-limited; back off.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `dvc` | Version control for datasets and models | https://dvc.org |
| `mlflow` | Experiment tracking, model registry | https://mlflow.org |
| `prophet` (Meta) | Time-series forecasting baseline | `pip install prophet` |
| `statsmodels` / `lifelines` | Survival/hazard models for completion forecasting | `pip install lifelines` |
| `xgboost` / `lightgbm` / `catboost` | Tabular gradient boosting | `pip install lightgbm` |
| `shap` | Feature attribution for explainability | `pip install shap` |
| `pandas` / `polars` / `duckdb` | Tabular wrangling | standard |
| `jira-cli` / `glab` / `gh` / `linear` | Issue exporters | per tool |
| `papermill` | Parameterized notebook runs for forecast generation | `pip install papermill` |
| `evidently` | Calibration + drift dashboards | https://github.com/evidentlyai/evidently |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Atlassian Atlas + Jira Insights | SaaS | REST | Native predictive forecasts; opaque, but easy. |
| Microsoft Project for the Web + Power BI | SaaS | Graph + REST | Forecast widgets, model authoring in Power BI. |
| GitLab Value Stream Analytics + Insights | SaaS/OSS | GraphQL | Cycle / DORA metrics with forecasting. |
| Azure DevOps Analytics (OData) | SaaS | OData | Powerful query surface for ML. |
| LinearB / Swarmia / Sleuth | SaaS | REST | Engineering-metrics with predictive overlays. |
| Plandek | SaaS | REST | Delivery-forecast tooling for SAFe orgs. |
| Tableau / Power BI / Looker | SaaS | REST | Visualization layer; pair with model output. |
| Databricks / Snowflake / BigQuery ML | SaaS | SQL | Train models close to the data. |
| Hugging Face Inference / OpenAI / Anthropic | SaaS | REST | LLM layer for analyst briefs (not point forecasts). |
| MLflow Tracking Server (self-host) | OSS | REST | Model + run versioning. |

## Templates & scripts
README is short; the methodology is data-pipeline-shaped. Inline below: a calibration check script for a probabilistic forecast.

```python
#!/usr/bin/env python3
"""calibration.py — check predicted-probability calibration on a holdout."""
from __future__ import annotations
import json, sys
import pandas as pd
from sklearn.calibration import calibration_curve

def main(path: str) -> int:
    df = pd.read_parquet(path)  # cols: y_true (0/1), y_prob (0..1)
    prob_true, prob_pred = calibration_curve(df["y_true"], df["y_prob"], n_bins=10)
    # Brier score
    brier = ((df["y_prob"] - df["y_true"]) ** 2).mean()
    out = {
        "brier": float(brier),
        "calibration_table": list(zip(map(float, prob_pred), map(float, prob_true))),
        "ok": float(brier) < 0.20,  # threshold tuned per project
    }
    print(json.dumps(out, indent=2))
    return 0 if out["ok"] else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
```

## Best practices
- Define the decision the forecast supports before training; if no decision changes with the forecast, do not build it.
- Start with naive baselines (last-3-sprints velocity, mean cycle time) — only ship a model that beats them on holdout, with statistical significance.
- Calibrate probabilistic outputs; report both the prediction and its reliability diagram each release.
- Always include feature attribution (SHAP) in stakeholder briefs; opaque scores destroy trust.
- Retrain on a fixed cadence (monthly) AND on drift triggers; track both.
- Human-in-the-loop for any action — model recommends, human decides — especially for resource changes.
- Aggregate at team or program level, not per individual; prevents misuse for performance management.
- Log every forecast with input snapshot for post-hoc audit; PM forecasts are revisited frequently.
- Pair predictive output with `value-stream-management/` flow metrics and `dora-metrics/` for triangulation.
- Document model assumptions in a model card; PMs and execs need to understand limits.

## AI-agent gotchas
- LLMs asked "predict when this will finish" hallucinate confident dates; force them to emit only ranges with explicit "model output X says" citations.
- Per-person productivity outputs are an HR landmine — refuse to generate; aggregate to team or workstream.
- Calibration drifts silently; without monitoring agents will keep forecasting poorly with high confidence.
- LLMs love to weave causal claims ("Bob's stories slip because Bob is overloaded") from purely correlational features. Strip causal language.
- Survivorship bias: training data excludes cancelled projects; agents will under-predict cancellation risk. Add explicit cancellation labels.
- Privacy: comment text used as a feature can leak PII into model logs; redact before training.
- Stale snapshots: a forecast generated yesterday on data from a week ago is worthless; agents must show data-freshness timestamp.
- Auto-actioning a forecast (e.g., auto-escalating "at-risk") creates feedback loops in the data; route to humans.
- Power-BI/Tableau dashboards from agents often miss row-level security; verify before publishing.
- Human-in-the-loop checkpoints (mandatory): release of new model, threshold tuning, retraining cadence change, escalation rules.

## References
- Mik Kersten, "Project to Product" (2018) — flow metrics + analytics framing.
- Reinertsen, "The Principles of Product Development Flow" — queueing theory roots.
- Gawande, "The Checklist Manifesto" — for the human-in-loop case.
- DORA Accelerate (Forsgren, Humble, Kim) — DORA metrics origin.
- "Forecasting: Principles and Practice" (Hyndman & Athanasopoulos) — open textbook for time-series.
- Sibling methodologies: `value-stream-management/`, `dora-metrics/`, `jira-workflow-management/`, `ai-in-project-management/`.
