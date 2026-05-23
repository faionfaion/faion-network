---
slug: ads-attribution-models
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Configures attribution comparison (platform-reported / GA4-modeled / warehouse-deduped) across paid channels, with variance thresholds and quarterly geo-holdout incrementality tests.
content_id: "c78f838ce6618735"
complexity: deep
produces: config
est_tokens: 6500
tags: ["marketing", "attribution", "analytics", "multi-touch", "ga4", "pro"]
---
# Ads Attribution Models

## Summary

**One-sentence:** Configures attribution comparison (platform-reported / GA4-modeled / warehouse-deduped) across paid channels, with variance thresholds and quarterly geo-holdout incrementality tests.

**One-paragraph:** Each ad platform claims its own conversions with different windows + logic, so platform totals exceed actual sales by 30-80%. This methodology configures a unified comparison layer (platform / GA4 / warehouse) with 15% variance threshold for investigation, quarterly geo-holdout incrementality tests, and an auto-generated variance report. Output: attribution config spec + reconciliation pipeline + variance report template + incrementality test plan.

**Ефективно для:**

- Multi-channel paid manager з > $5k/mo і attribution mess.
- Quarterly budget review: defensible reconciled numbers замість platform sums.
- Geo-holdout incrementality test для true-incremental lift per channel.
- Auto-generated weekly variance report для exec audience.

## Applies If (ALL must hold)

- Multi-channel paid programs (2+ platforms) where totals don't match warehouse.
- GA4 + BigQuery (or equivalent warehouse) operational.
- Quarterly budget review cadence requiring defensible numbers.
- Marketing owner can authorize geo-holdout tests (2-4 weeks regional spend off).

## Skip If (ANY kills it)

- Single-channel paid spend — last-click works.
- No warehouse — implement ads-analytics-setup first.
- Spend < $5k/month — variance smaller than measurement error.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Inputs source-of-truth | system / dashboard / transcript | operator-managed |
| Prior artefact (if any) | Markdown / JSON / YAML | prior cycle |
| Named consumer for output | team contact / agent task | operator-managed |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/AGENTS.md` | parent group context (vocabulary, neighbours) |
| [[learnings-database-schema]] | shared cumulative-knowledge substrate (if available) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | >=5 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid + forbidden patterns | ~1000 |
| `content/03-failure-modes.xml` | essential | >=3 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with inputs / actions / outputs / decision-gates | ~1100 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping observable signals to a rule from 01-core-rules.xml | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision-tree application; bounded judgement. |
| `draft-ads-attribution-models` | opus | Synthesis under output contract; final write-up. |
| `validate-output` | haiku | Mechanical schema check via scripts/validate-<slug>.py. |

## Templates

| File | Purpose |
|------|---------|
| `templates/config.yaml` | YAML config skeleton with 5-line header |
| `templates/output.json` | JSON sidecar with __faion_header__ |
| `templates/_smoke-test.yaml` | Minimum viable filled config |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ads-attribution-models.py` | Validate the produced artefact against the JSON Schema in `content/02-output-contract.xml` | After subagent returns, before publish; pre-commit if artefact is git-tracked |

## Related

- [[ad-account-hygiene-checklist]]
- [[ads-attribution-models]]
- [[learnings-database-schema]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (inputs available, thresholds, gating prerequisites) to a concrete verdict, each leaf referencing a rule from `01-core-rules.xml`. Use it whenever multiple variants of the methodology look applicable, or when an upstream condition (e.g. positioning undefined, spend below threshold) makes the methodology a misfit.
