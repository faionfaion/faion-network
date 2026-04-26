# Earned Value Management

## Summary

Measure project schedule and cost performance objectively using PV (Planned Value), EV (Earned Value), and AC (Actual Cost). Derive variance indices (SPI, CPI) and forecasts (EAC, ETC, TCPI). The rule: use objective % complete only — milestones, units completed, or 0/50/100 rules — never subjective opinion, which corrupts EV and cascades into false forecasts.

## Why

"We're 80% done" is meaningless without context. EVM converts progress claims into objective financial metrics: CPI tells you the cost efficiency of work completed; SPI tells you schedule efficiency. CPI rarely improves spontaneously — a CPI < 0.9 sustained for two periods signals a structural problem, not noise. TCPI > 1.10 typically indicates the project is unrecoverable on current budget.

## When To Use

- Predictive/hybrid projects with a fixed scope baseline and budget
- Programs with monthly/weekly steering committee status reporting
- Government, defense, infrastructure, large IT — contracts requiring ANSI/EIA-748
- Engagements where "% complete" claims have lost credibility
- Program forecasting (EAC/ETC) for board approval of additional budget

## When NOT To Use

- Pure agile teams shipping continuously — burndown and flow metrics are better fits
- Discovery/R&D phases with no stable baseline to measure against
- Projects under 6 weeks or under $50k — overhead exceeds insight gained
- Internal startup work where speed matters more than financial control
- Soft-cost projects with no convertible-to-dollars effort tracking

## Content

| File | What's inside |
|------|---------------|
| `content/01-evm-metrics.xml` | Core metrics (PV/EV/AC/SPI/CPI/EAC/ETC/VAC/TCPI), formulas, interpretation thresholds |
| `content/02-evm-process.xml` | Four-step process: baseline, measure, calculate, forecast; common mistakes; agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/evm-dashboard.md` | EVM status report with metrics table, variances, forecasts, and status color |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/evm.py` | Pure EVM calculator: inputs WP bac/pct_planned/pct_complete/ac, outputs full metric set |
| `scripts/eac-montecarlo.py` | Three-point EAC under uncertainty via triangular Monte Carlo simulation |
