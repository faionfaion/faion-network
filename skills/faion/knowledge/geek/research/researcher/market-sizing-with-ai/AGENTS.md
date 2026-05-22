---
slug: market-sizing-with-ai
tier: geek
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI-assisted TAM/SAM/SOM estimation using top-down and bottom-up triangulation, with explicit assumption documentation and confidence ratings per data point.
content_id: "df0686b1577da57d"
tags: [market-sizing, tam-sam-som, triangulation, ai-assisted, research]
---
# Market Sizing with AI

## Summary

**One-sentence:** AI-assisted TAM/SAM/SOM estimation using top-down and bottom-up triangulation, with explicit assumption documentation and confidence ratings per data point.

**One-paragraph:** AI-assisted TAM/SAM/SOM estimation using top-down and bottom-up triangulation, with explicit assumption documentation and confidence ratings per data point. Both paths must run independently; result is accepted only when they are within 2-3x of each other.

## Applies If (ALL must hold)

- Early-stage TAM/SAM/SOM validation before an investor deck or strategic decision.
- Triangulating conflicting market estimates from multiple sources.
- Generating a bottom-up model from known unit economics (ICP count, ACV, churn).
- Stress-testing existing market assumptions when entering a new segment.
- Supplementing a market researcher's draft with AI-fetched data points.

## Skip If (ANY kills it)

- Sole input for a fundraising pitch without primary source validation — LLMs hallucinate market figures.
- Nascent markets (under 3 years old) with no industry reports — AI-synthesized data lacks grounding.
- When regulatory or geographic precision is critical (e.g., healthcare TAM per country) — estimates too coarse.
- High-stakes M&A diligence — hire a research analyst; speed does not justify precision loss.

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

- parent skill: `geek/research/researcher/`
