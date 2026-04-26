# Risk Register

## Summary

A living log of identified threats and opportunities, each with a probability (1–5), impact (1–5), risk score (P×I), chosen response strategy, named owner, trigger condition, and current status. The register must be reviewed weekly and updated as risks materialize, pass, or merge.

## Why

Without a documented register, risks have no accountability — every risk becomes a surprise crisis. Stale registers with no owners and "All Accept" strategies provide false comfort. The register forces explicit owner assignment, measurable triggers, and funded contingency, turning reactive fire-fighting into managed uncertainty.

## When To Use

- Multi-month delivery requiring a single source of truth for risks across teams.
- Audited or regulated programs needing a register with IDs, owners, and decision history.
- Programs with quantitative contingency reserves that must be defended to finance.
- Cross-vendor or cross-org work where risks span ownership boundaries.

## When NOT To Use

- Solo or hobby projects — a `RISKS.md` checklist is enough.
- Pure-Scrum teams running impediment and retro loops with adequate coverage.
- Spike or discovery work where most "risks" are research questions.

## Content

| File | What's inside |
|------|---------------|
| `content/01-risk-process.xml` | Six-step process: identify (categories + techniques), analyze (P/I scales), score (5×5 matrix), plan responses (threat and opportunity strategies), assign owners, monitor weekly. |
| `content/02-examples-antipatterns.xml` | Worked examples (software project threats, opportunity risks); antipatterns for one-time exercise, no owners, all-accept, missing opportunities, vague descriptions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/risk-register.md` | Full register table: ID, description, category, P, I, score, strategy, response, owner, status. |
| `templates/risk-card.md` | Individual risk card with assessment, response plan, contingency, trigger, and tracking log. |
| `templates/risk-audit.py` | Script that flags stale (>14 days, open), high-priority (score ≥ 15), and no-owner risks from a CSV register. |
