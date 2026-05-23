---
slug: competitor-analysis
tier: pro
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 5-step framework (identify -> map -> analyse -> gap -> differentiate) producing competitive-analysis.md across direct/indirect/future competitors on 8 dimensions, ending in a sourced positioning statement.
content_id: "5794e42b1ecd42cf"
complexity: medium
produces: report
est_tokens: 5400
tags: [competitor-analysis, positioning, market-research, differentiation, gap-analysis]
---
# Competitor Analysis

## Summary

**One-sentence:** 5-step framework (identify -> map -> analyse -> gap -> differentiate) producing competitive-analysis.md across direct/indirect/future competitors on 8 dimensions, ending in a sourced positioning statement.

**One-paragraph:** Systematic 5-step framework for studying competitors: identify direct (5-10), indirect (3-5), and future (2-3); plot on a price-vs-feature-breadth positioning matrix; analyse across 8 dimensions (Product, Pricing, Positioning, Technology, Traction, Team, Marketing, Weaknesses); convert top complaints into a gap analysis; emit a positioning statement that names the competitor. Output is competitive-analysis.md.

**Ефективно для:**

- Pre-MVP: 5-10 candidate-конкурентів ідентифіковано, треба structured scan.
- Positioning sprint: переписуєте landing page або pricing.
- New feature greenlight: треба порівняти implementation у 3-7 incumbents.
- Quarterly market refresh: re-score price/features/traction.
- Pitch deck: будуєте competitor matrix slide з gaps.

## Applies If (ALL must hold)

- Pre-MVP: 5-10 candidate competitors identified; need structured scan before committing engineering time.
- Positioning sprint: landing page or pricing rewrite requires a defensible differentiation statement.
- New-feature greenlight: comparing how 3-7 incumbents implement a feature you plan to build.
- Quarterly market refresh: re-scoring known competitors on price, features, and traction.
- Investor / pitch deck: building a credible competitor matrix slide with named gaps.

## Skip If (ANY kills it)

- Deep customer-pain discovery - competitors are a proxy; use pain-points first.
- Pure brainstorming with no category defined yet - run idea-generation first.
- Regulated / B2B-enterprise procurement where pricing is hidden behind sales.
- Real-time monitoring of a single competitor - use a change-tracking service.
- 'Should we build this?' gut checks - competitor count alone does not answer that.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Seed competitor list | YAML / markdown | founder + customer interviews |
| Target geography | ISO country code | GTM doc |
| Category definition | one sentence | positioning doc |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[market-research-tam-sam-som]] | supplies the category boundary used to qualify competitor inclusion |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `identify-competitors` | haiku | Mechanical SERP + Product Hunt + G2 enumeration. |
| `per-competitor-snapshot` | haiku | Fan-out fill of snapshot template. |
| `weakness-extraction` | sonnet | Read 1-star reviews + Reddit; pick top-3 complaints. |
| `gap-and-positioning` | opus | Strategic synthesis: gap type + positioning statement. |

## Templates

| File | Purpose |
|------|---------|
| `templates/competitor-report.md` | Full analysis report skeleton (matrix + gap analysis + differentiation) |
| `templates/competitor-snapshot.md` | Single-competitor snapshot template for parallel sub-tasks |
| `templates/scrape-competitor.sh` | Bash scraper: homepage + pricing + G2 + Wayback for one competitor |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-competitor-analysis.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[competitive-intelligence]]
- [[market-research-tam-sam-som]]
- [[persona-building]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
