---
slug: ai-earned-value-management
tier: geek
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "4eee33ef19b779c3"
summary: Auto-compute PV/EV/AC and SPI/CPI weekly by ingesting Git commit volume, Jira completion, budget burn, and invoice cadence — replacing manual EVM entry with a sensor-driven pipeline that publishes a confidence interval, not a single point estimate.
tags: [evm, project-management, earned-value, ai-pm, geek]
---
# AI Earned-Value Management

## Summary

**One-sentence:** A sensor-driven EVM pipeline that ingests Git commit volume, Jira / Linear completion, budget burn, and invoice cadence to auto-compute PV (Planned Value), EV (Earned Value), AC (Actual Cost), and the SPI / CPI indices weekly — with an explicit confidence interval.

**One-paragraph:** The classic `earned-value-management` methodology and `evm.py` script require manual PV / EV / AC entry every reporting cycle. In practice the PM forgets, mis-keys, or skips, and the variance metrics decay into theatre. The AI variant turns EVM into a continuous pipeline: a Git sensor (commits + diff size + reviewed-merge events), a tracker sensor (Jira / Linear story-point completion), a finance sensor (budget-tool cost rollup), and an invoice sensor (vendor / contractor pay events) feed into a weekly aggregator that produces SPI / CPI with a bootstrap-style confidence band derived from the noise of the historical sensors. Output: a one-row weekly EVM report that the PM reviews and signs off — never auto-published — with red / yellow / green bands tied to action.

## Applies If (ALL must hold)

- Project has a baseline plan with planned work units mapped to dates (Gantt, milestone list, or burn-down).
- Project has &gt;= 1 of: Git repo with semantic commits, Jira / Linear / ClickUp with story points, budget tool (Lever, custom spreadsheet).
- Reporting cadence is weekly or bi-weekly and a PM owns the report.
- Project duration is &gt;= 6 weeks (shorter projects use burn-down; EVM math is meaningless on 2-week sprints).

## Skip If (ANY kills it)

- Project is &lt; 6 weeks total — EVM overhead exceeds the win; use a burn-down chart.
- Pure agile team with no fixed baseline plan — EVM requires PV, which requires a baseline.
- Single-developer hobby project — sensor noise dominates the signal at n=1.
- Internal R&amp;D with no fixed budget — AC has no meaning.

## Prerequisites

- Baseline plan exported as `baseline.json`: work units with dates, planned cost, and story-point or LoE weights.
- Git access (read-only) and Jira / Linear API token.
- Budget tool API token or weekly cost CSV export.
- A scheduled job runner (cron, GitHub Actions, scheduled Claude SDK agent).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager/earned-value-management` | Classic EVM definitions (PV, EV, AC, SPI, CPI); this methodology consumes them. |
| `geek/pm/project-manager/ai-powered-pm-tools` | Survey of PM-tool AI integrations; this is the concrete EVM realisation. |
| `pro/pm/project-manager/risk-register` | RAG bands feed into the risk register weekly. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: baseline immutability, sensor independence, confidence interval requirement, signed-off-by-PM gate, weekly cadence | ~1100 |
| `content/02-output-contract.xml` | essential | Weekly EVM report schema, RAG band rules, sensor freshness floor | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: sensor noise, story-point inflation, stale baseline, invoice lag, AI-confidence overclaim | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `git-sensor-aggregate` | haiku | Mechanical commit / diff / merge aggregation |
| `tracker-sensor-aggregate` | haiku | Story-point completion sums; rules-only |
| `pv-ev-ac-compute` | sonnet | Bounded judgment: map sensor reads to PV/EV/AC formula |
| `confidence-interval-and-rag-band` | sonnet | Bootstrap CI from historical noise; RAG band assignment |
| `weekly-report-narrative` | opus | Synthesis paragraph for the PM; cross-sensor narrative |

## Templates

| File | Purpose |
|------|---------|
| `templates/baseline.json` | Schema for the project baseline: work units, dates, weights, planned cost |
| `templates/evm-weekly.json` | Schema for the weekly EVM record |
| `templates/pm-signoff.md` | PM signoff line template with required reviewer fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/sensors/git.py` | Pull commit / diff / merge events for the reporting week | Weekly |
| `scripts/sensors/jira.py` | Pull story-point completion events from Jira / Linear | Weekly |
| `scripts/sensors/finance.py` | Pull cost rollup from budget tool | Weekly |
| `scripts/compute-evm.py` | Compute PV / EV / AC / SPI / CPI from sensor outputs; emit weekly record | After sensors complete |
| `scripts/confidence-band.py` | Bootstrap CI over last 8 weeks of sensor noise | Inside compute-evm.py |

## Related

- parent skill: `geek/pm/project-manager/`
- peer methodologies: `ai-powered-pm-tools`, `ai-pm-tool-integration-recipes`
- external: [PMI Earned Value Management (PMBOK 7)](https://www.pmi.org/) · [Beyond EVM (NASA SP-2015-3424)](https://ntrs.nasa.gov/) · [Linear API](https://developers.linear.app/)
