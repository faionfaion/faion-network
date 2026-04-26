# Earned Value Management

## Summary

Earned Value Management (EVM) measures project performance by integrating scope, schedule, and cost into three numbers — Planned Value (PV), Earned Value (EV), and Actual Cost (AC) — and derives objective indices (SPI, CPI) and forecasts (EAC, TCPI) that predict final cost and completion date. All computation is deterministic; LLMs narrate, they never calculate.

## Why

Traditional "percent spent" and "percent done" metrics are independently uninterpretable. EVM relates them: CPI = EV/AC tells you how much value you get per dollar spent; SPI = EV/PV tells you how far behind or ahead you are. CPI rarely improves on its own — an early CPI of 0.73 predicts a 37% overrun with high reliability. This gives sponsors a data-based escalation trigger, not a gut feeling.

## When To Use

- Fixed-price or cost-plus contracts requiring DCMA/DCAA compliance (defense, aerospace, government).
- Capital programs with multi-year baselines where SPI/CPI trends feed quarterly board reporting.
- Programs where percent-complete claims have been chronically inflated.
- Hybrid/agile programs that still need finance-grade burn forecasts (EAC, ETC, VAC) tied to velocity.
- Portfolio reporting where many projects feed a single rollup.

## When NOT To Use

- Pre-PMF startups or pure agile teams without baseline budgets — EVM math is meaningless without a credible PV curve.
- Time-and-materials contracts where only AC matters — EVM adds overhead with no decision impact.
- Discovery or spike phases where "percent complete" is undefined.
- Projects under one quarter with a single team — burndown and weekly retro provide the same insight cheaper.
- Projects without WBS or work-package-level budgets — EVM rolls up from packages; without them the metrics are fiction.

## Content

| File | What's inside |
|------|---------------|
| `content/01-metrics.xml` | Core EVM metrics (PV/EV/AC/SV/CV/SPI/CPI/EAC/ETC/VAC/TCPI) with formulas and interpretation |
| `content/02-process.xml` | Step-by-step: establish baseline, measure progress, calculate indices, forecast completion, earn recognition rules |
| `content/03-rules.xml` | Rules for earning rules, re-baselining discipline, TCPI escalation, and agentic EVM workflow |

## Templates

| File | Purpose |
|------|---------|
| `templates/evm-report.md` | EVM dashboard template: key metrics, variances, forecasts, RAG status |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/evm_calc.py` | Deterministic EVM index computation from baseline.yaml + actuals.yaml; outputs JSON |
