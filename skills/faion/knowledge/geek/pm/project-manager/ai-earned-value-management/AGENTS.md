---
slug: ai-earned-value-management
tier: geek
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: "Auto-computes weekly PV/EV/AC + SPI/CPI by ingesting Git commit volume, Jira completion, budget burn, invoice cadence — confidence-interval EVM, not point estimates."
content_id: "b7d35dae7413261d"
complexity: deep
produces: report
est_tokens: 4200
tags: [evm, ai-pm, earned-value, automation, sensor-driven]
---
# Ai Earned Value Management

## Summary

**One-sentence:** Auto-computes weekly PV/EV/AC + SPI/CPI by ingesting Git commit volume, Jira completion, budget burn, invoice cadence — confidence-interval EVM, not point estimates.

**One-paragraph:** Auto-computes weekly PV/EV/AC + SPI/CPI by ingesting Git commit volume, Jira completion, budget burn, invoice cadence — confidence-interval EVM, not point estimates. The methodology is anchored to a single named consumer (a PM, EM, portfolio owner, or downstream agent) and a fixed-shape artefact that downstream review can sign off without re-deriving reasoning. Inputs are explicit, evidence is anchored, and the artefact carries `version`, `owner`, and `last_reviewed` so it remains a living operating tool rather than folklore. Outputs that fail the contract are rejected at validation time, not at executive review.

**Ефективно для:** PM-у — щоб EVM не залежав від ручного оновлення статусу, а тек з реальних подій з опресувальним CI.

## Applies If (ALL must hold)

- Project tracks EVM (PV/EV/AC) and has stable WBS.
- Git + tracker + budget feeds are accessible via API.
- Named PM owns the weekly EVM publish.
- Project duration ≥ 6 weeks (CI needs samples).

## Skip If (ANY kills it)

- Project < 6 weeks — insufficient samples for CI to be meaningful.
- No tracker / budget API — manual EVM remains the only option.
- Team rejects EVM as a frame (lean-startup, #NoEstimates).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Git API access | token | GitHub / GitLab |
| Tracker API access | token | Jira / Linear |
| Budget feed | API/CSV | finance system |
| WBS + PV baseline | spreadsheet | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/pm/ev-for-fixed-bid-outsource` | Dual-ledger model the AI EVM feeds. |
| `geek/pm/portfolio-evm-rollup-method` | Portfolio rollup the auto-EVM aggregates into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules every application enforces | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom / root-cause / fix | ~900 |
| `content/06-decision-tree.xml` | essential | Root question → branches → conclusions (rule refs) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `metric-pull-and-compute` | haiku | Pure pipeline math. |
| `confidence-interval-fit` | sonnet | Bounded judgement: pick distribution shape. |
| `pm-narrative` | opus | Variance write-up with traceable evidence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.py` | Python skeleton: pull Git+Jira+budget → compute PV/EV/AC → CI estimate → JSON output. |
| `templates/header.yaml` | Frontmatter contract: owner, version, last_reviewed for the produced artefact. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-earned-value-management.py` | Validate produced artefact against the JSON Schema in `02-output-contract.xml`. | Pre-merge and on every artefact refresh. |

## Related

- [[ev-for-fixed-bid-outsource]]
- [[portfolio-evm-rollup-method]]
- [[ai-pm-tool-integration-recipes]]

## Decision tree

The mandatory decision tree at `content/06-decision-tree.xml` Decides whether to wire the AI EVM pipeline (stable WBS + APIs + ≥6 weeks), block (no APIs), or skip (short project). Run before the first weekly EVM run is scheduled.
