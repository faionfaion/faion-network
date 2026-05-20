---
slug: market-analysis
tier: pro
group: research
domain: market-researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Market analysis is the combined methodology for sizing a market (TAM/SAM/SOM), classifying trend timing, mapping the competitive landscape (15-20 named players with URLs), and producing a feature-gap matrix from the top 5 competitors.
content_id: "b042dfdfad1d4936"
tags: [market-sizing, competitive-landscape, feature-matrix, tam-sam-som, trend-analysis]
---
# Market Analysis

## Summary

**One-sentence:** Market analysis is the combined methodology for sizing a market (TAM/SAM/SOM), classifying trend timing, mapping the competitive landscape (15-20 named players with URLs), and producing a feature-gap matrix from the top 5 competitors.

**One-paragraph:** Market analysis is the combined methodology for sizing a market (TAM/SAM/SOM), classifying trend timing, mapping the competitive landscape (15-20 named players with URLs), and producing a feature-gap matrix from the top 5 competitors. The core rule: run both top-down and bottom-up sizing; if they diverge more than 2x, flag it as a research gap rather than averaging. These four sub-methodologies share data sources and produce JSON-first outputs that feed downstream SDD artifacts.

## Applies If (ALL must hold)

- Before writing a spec.md for a new product idea — produces SAM number and competitive whitespace
- When the GTM strategist or product manager needs a quantified opportunity ($X M SAM, Y% CAGR, Z named competitors)
- Quarterly competitor refresh: re-scrape pricing pages, changelogs, review sites for moves
- Pre-fundraise: investor decks need a defensible TAM and a feature matrix
- Niche viability scoring inside niche-evaluation flows — replaces guesses with sourced numbers

## Skip If (ANY kills it)

- Single-customer custom builds with no market
- Pure technical or architecture research — route to pro/dev/software-architect instead
- Ideas fewer than 2 weeks from launch where research will not change the decision
- Highly regulated B2B niches (defense, medical devices) where public data is scarce — use primary expert interviews
- Working business where the decision is growth, not entry — switch to growth-marketer or conversion-optimizer

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

- parent skill: `pro/research/market-researcher/`
