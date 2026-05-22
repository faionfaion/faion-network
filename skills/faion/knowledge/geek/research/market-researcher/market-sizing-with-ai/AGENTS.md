---
slug: market-sizing-with-ai
tier: geek
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI-assisted TAM/SAM/SOM estimation via top-down and bottom-up triangulation.
content_id: "df0686b1577da57d"
tags: [market-sizing, tam-sam-som, triangulation, ai-research, estimation]
---
# Market Sizing with AI

## Summary

**One-sentence:** AI-assisted TAM/SAM/SOM estimation via top-down and bottom-up triangulation.

**One-paragraph:** AI-assisted TAM/SAM/SOM estimation via top-down and bottom-up triangulation. Run both methods independently using separate Perplexity and web-search calls, document every assumption, then triangulate: if both paths agree within 2x, confidence is defensible; if not, flag the divergence and identify the assumption driving the gap. Output a structured estimate with confidence ranges, not point numbers.

## Applies If (ALL must hold)

- Producing TAM/SAM/SOM estimates to support a go/no-go decision or investor deck
- Triangulating market size when no single authoritative report exists
- Stress-testing existing market estimates by running independent top-down and bottom-up paths
- Automating recurring market-size updates as part of a research cadence

## Skip If (ANY kills it)

- When the investor or client requires named analyst reports (Gartner, IDC) — AI cannot substitute these
- Highly novel markets with less than 12 months of public data — AI extrapolates from unreliable proxies
- Regulated contexts (IPO prospectus, SEC filing) where every number needs traceable sourcing
- When the market boundary is contested — AI anchors to the most common framing without flagging ambiguity

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

- parent skill: `geek/research/market-researcher/`
