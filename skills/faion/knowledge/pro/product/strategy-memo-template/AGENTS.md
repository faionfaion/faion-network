---
slug: strategy-memo-template
tier: pro
group: product
domain: product
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "9ab3812f06a0df0c"
summary: "Produces a 2-page strategy memo (vision, bets, non-bets, success metrics) that replaces 40-slide decks for annual product strategy refresh."
tags: [strategy-memo-template, product, pro]
---
# Strategy Memo Template

## Summary

**One-sentence:** Produces a 2-page strategy memo (vision, bets, non-bets, success metrics) that replaces 40-slide decks for annual product strategy refresh.

**One-paragraph:** Reforge/Lenny-style strategy memo: forces a PM to fit annual direction onto one page of vision + one page of three numbered bets, each with a falsifiable success metric and an explicit anti-bet. Mechanism: structured template + 3-stakeholder pre-read + 60-min walk-through. Primary output: signed memo URL with version + decision-owner.

## Applies If (ALL must hold)

- annual or H1/H2 product-strategy cycle is live
- ≥1 prior quarter of product metrics is available for grounding
- named decision-owner exists (head of product, founder, or GM)

## Skip If (ANY kills it)

- company has <3 months of usage data — too early for falsifiable bets
- no decision-owner — memo becomes a brainstorm with no commitment
- team already runs OKRs with explicit bets — duplication risk

## Prerequisites

- last 4 quarters of product metrics (DAU/WAU, retention, NPS, revenue)
- current roadmap export (Linear/Jira/Notion)
- calendar holds for 3 stakeholder pre-reads

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product` | parent domain group — provides operating context for Strategy Memo Template |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/strategy-memo-template.json` | JSON schema for the Strategy Memo Template output contract |
| `templates/strategy-memo-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-strategy-memo-template.py` | Enforce Strategy Memo Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/product/`
- upstream playbook: `role-product-manager/Annual product strategy refresh`
- solo/product/product-planning/portfolio-strategy
- solo/product/product-manager/outcome-based-roadmaps-advanced
