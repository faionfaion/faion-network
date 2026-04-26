# Predictive Analytics in PM

## Summary

Apply machine learning to historical project data to generate early-warning signals for schedule slip, budget overrun, resource contention, and material price risk — turning raw PM telemetry into probability-interval forecasts that change PMO decisions before events occur. The analytics layer lives in a separate ML pipeline feeding the PM tool through alerts and dashboards; humans retain all decision authority.

## Why

Reactive PM catches problems at post-mortem; predictive analytics catches them 2-6 weeks earlier. Studies show well-implemented ML-based schedule forecasting reduces cost overruns by ~15% on comparable portfolio programs. Reference-class forecasting (Flyvbjerg) is the required baseline — if ML cannot beat it, ML is not worth the data-plumbing cost.

## When To Use

- Portfolio of 50+ comparable projects with 12+ months of clean historical data (issues, time logs, budget actuals)
- Construction, engineering, manufacturing, or infrastructure programs where slip and overrun are repeat offenders
- PMO needs early-warning dashboard and executive trend signals
- Vendor/commodity-heavy programs where price volatility (steel, cloud spend) drives budget risk
- EVM already in place and the org wants an ML complement for interval forecasting

## When NOT To Use

- Portfolio under 10 projects — sample size is too small; use heuristics + EVM instead
- Brand-new project type with no historical analogues — no training data; use reference-class forecasting alone
- Highly creative or one-off work (research, novel product) — past patterns do not generalize
- Organisation without basic data hygiene (inconsistent statuses, missing actuals, freeform fields) — fix data first
- Goal is optics ("look modern") rather than changing actual PMO decisions — model value requires action on output

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | ML application areas, data quality requirements, human-in-the-loop mandate |
| `content/02-workflow.xml` | Agentic pipeline architecture, subagent roles, prompt patterns, AI-agent gotchas |
| `content/03-tools-and-references.xml` | CLI tools, SaaS services, best practices, key references |

## Templates

| File | Purpose |
|------|---------|
| `templates/slip-baseline.py` | Baseline GBR schedule-slip regressor (scikit-learn, GroupKFold, SHAP-ready) |
| `templates/data-contract.yaml` | Feature contract schema for the data-contract agent |
