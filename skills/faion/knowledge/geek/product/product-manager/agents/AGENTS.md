---
slug: agents
tier: geek
group: product
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Two Claude subagents for product scoping work: faion-mvp-scope-analyzer-agent analyzes competitor features to recommend a minimum feature set for a new product; faion-mlp-agent upgrades an MVP to an MLP (Minimum Lovable Product) through a five-mode sequential pipeline (analyze → find-gaps → propose → update → plan).
content_id: "37259ea365fc4323"
tags: [product-agents, mvp, mlp, competitor-analysis, product-planning]
---
# Product Manager Agents

## Summary

**One-sentence:** Two Claude subagents for product scoping work: faion-mvp-scope-analyzer-agent analyzes competitor features to recommend a minimum feature set for a new product; faion-mlp-agent upgrades an MVP to an MLP (Minimum Lovable Product) through a five-mode sequential pipeline (analyze → find-gaps → propose → update → plan).

**One-paragraph:** Two Claude subagents for product scoping work: faion-mvp-scope-analyzer-agent analyzes competitor features to recommend a minimum feature set for a new product; faion-mlp-agent upgrades an MVP to an MLP (Minimum Lovable Product) through a five-mode sequential pipeline (analyze → find-gaps → propose → update → plan). The MLP dimensions are Delight, Ease, Speed, Trust, and Personality.

## Applies If (ALL must hold)

- Defining MVP scope for a new product where competitor analysis is needed to determine the minimum feature set
- Upgrading an MVP to an MLP (Minimum Lovable Product) by identifying the "WOW" features that differentiate the product
- Running a structured gap analysis between current product state and MLP targets before a roadmap planning session
- Updating spec files with MLP requirements after a gap analysis or discovery session
- Sequencing MLP feature implementation when multiple WOW features are identified and need to be prioritized

## Skip If (ANY kills it)

- Product is at ideation stage only — no existing specs or MVP definition to analyze; start with discovery methodology instead
- Competitor landscape is entirely novel and no comparable products exist; the MVP scope analyzer needs comparables to work from
- Team is not ready to act on spec updates (e.g., mid-sprint, code freeze); run mode: analyze and mode: find-gaps for prep, defer mode: update until the team is ready
- The product is B2B enterprise with highly custom requirements; cookie-cutter MLP dimensions (Delight, Ease, Speed, Trust, Personality) may not apply without modification

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/product/product-manager/`
