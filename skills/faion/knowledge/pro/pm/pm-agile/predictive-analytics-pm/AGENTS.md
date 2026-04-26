# Predictive Analytics in PM

## Summary

The application of ML-based forecasting to project management: schedule delay early warning, budget overrun detection, resource utilization optimization, and risk pattern mining from issue tracker data. Requires a deterministic data pipeline (extract → feature-build → classical ML model) with an LLM layer only for plain-language briefs. The LLM never produces the point forecast; a calibrated model does.

## Why

Naive baselines (last-3-sprint velocity, mean cycle time) are the floor — only deploy a model that beats them on a holdout with statistical significance. Human intuition on schedule risk lags 3–5 days behind what burn-down data already implies; a properly calibrated model can surface "this sprint will miss" with actionable lead time. Privacy and survivorship bias are the two most common failure modes: aggregate at team level, include cancelled projects in training data.

## When To Use

- Backlogs and historical data large enough (at least 200 closed items, 6+ months) for forecasting to beat naive baselines.
- Schedule risk early-warning: detect sprint misses 3–5 days before the burn-down does.
- Budget overrun detection: compare run-rate trends with planned spend.
- Resource utilization optimization across multi-team programs.
- Risk pattern mining: find leading indicators (epic age, comment sentiment, churn) of late delivery.

## When NOT To Use

- Small teams or new projects without historical data — models will overfit or underperform expert estimation.
- Hand-managed spreadsheets without consistent fields — data quality kills the signal.
- Decision-making needing explainability you cannot provide (regulated procurement, public-sector audits).
- "AI dashboards" stakeholders cannot read — predictive output without a human translator becomes shelf-ware.
- When the underlying issue is organizational (priorities flip weekly) — no model fixes leadership decisions.

## Content

| File | What's inside |
|------|---------------|
| `content/01-analytics-pipeline.xml` | Four-agent pipeline: data-extractor, feature-builder, forecast-runner (classical ML, not LLM), analyst-agent (LLM for briefs). Calibration requirement, drift monitoring, human-in-loop checkpoints. |
| `content/02-antipatterns.xml` | Seven ML-in-PM antipatterns: garbage-in status fields, concept drift, survivorship bias, uncalibrated probabilities, causation vs. correlation, per-person metrics, stale snapshot forecasts. |

## Templates

| File | Purpose |
|------|---------|
| `templates/calibration.py` | Calibration check script: Brier score and calibration curve against a parquet holdout set. |
