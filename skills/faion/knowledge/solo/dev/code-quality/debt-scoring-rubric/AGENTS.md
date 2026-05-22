---
slug: debt-scoring-rubric
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "c0dcc1add6f06b45"
summary: Five-factor scoring rubric (User-Impact × Change-Frequency × Fragility × Blast-Radius × Fix-Cost) that produces a single numeric debt score per item, defensible to PMs and the org.
tags: [tech-debt, scoring, prioritization, architecture-debt, design-debt]
---

# Debt Scoring Rubric

## Summary

**One-sentence:** Five-factor scoring rubric (User-Impact × Change-Frequency × Fragility × Blast-Radius × Fix-Cost) that produces a single numeric debt score per item, defensible to PMs and the org.

**One-paragraph:** Solves the recurring "we know we have debt but can't defend the sprint scope" problem. Mechanism: each debt item is scored 1-5 on five factors with explicit anchors per score; the rubric returns score = (User-Impact × Change-Frequency × Fragility × Blast-Radius) / Fix-Cost, plus a confidence band. Items above the team's prioritization threshold enter the next debt sprint; below-threshold items are logged in the debt register with the score so they can be re-evaluated later. Primary output: a ranked debt list with score, confidence, and one-line "what changes if we pay this".

## Applies If (ALL must hold)

- team_or_individual maintains an existing codebase / design system / infrastructure
- at least 5 candidate debt items have been collected (single-item scoring is overhead)
- prioritization audience is a PM / client / stakeholder who needs a defensible ranking
- debt category ∈ {architecture, code, test, design, infra, dependency, documentation}

## Skip If (ANY kills it)

- greenfield project &lt; 3 months old — debt baseline does not exist, use minimum-product-frameworks instead
- single-developer experiment with no production users — score has no business meaning
- urgent security or compliance debt — these have a separate must-do classification, not a scored ranking
- &gt; 100 candidate items at once — first triage with the boy-scout / opportunistic rules from tech-debt-management before scoring

## Prerequisites

- written list of candidate debt items, each with a one-line description and a code/design pointer
- baseline metrics available: change-frequency from git log, fragility from incident/bug count per area, blast-radius from service map or dependency graph
- agreement with the prioritization audience on what "User-Impact 5" means in this product (anchor calibration)
- a debt register file (CSV / Notion / Linear / Jira) to record scored items

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/code-quality/tech-debt-management` | Defines payoff strategies and CI gates this rubric feeds into |
| `free/dev/code-quality/code-review-process` | Source of bug/incident counts used in the Fragility factor |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: factor definitions, anchor scale, formula, confidence band, audience-defensibility | ~1300 |
| `content/02-output-contract.xml` | essential | Scored-item schema, forbidden patterns, register schema | ~600 |
| `content/03-failure-modes.xml` | essential | 6 LLM/agent failure modes when applying the rubric | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `metric_extraction_per_item` | haiku | Pull change-frequency / bug-count from existing data stores |
| `per-factor_scoring` | sonnet | Bounded judgment per anchor; can read code context |
| `cross-item_ranking_review` | opus | Catch over-anchoring drift across the whole list |

## Templates

| File | Purpose |
|------|---------|

## Scripts

| File | Purpose |
|------|---------|

## Related

- parent skill: `solo/dev/code-quality/SKILL.md`
- peer methodologies: `solo/dev/code-quality/tech-debt-management`, `pro/dev/code-quality/architecture-decision-records`
- external: [Martin Fowler — TechnicalDebtQuadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant.html) · [Ward Cunningham — Debt Metaphor (1992)] · [Adam Tornhill "Your Code as a Crime Scene" change-frequency analysis] · [Google SRE workbook — toil and tech debt]
