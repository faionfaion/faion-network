---
slug: perplexity-ai-research
tier: geek
group: research
domain: researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A workflow for using Perplexity Pro Search to synthesize cited multi-source research answers.
content_id: "dc8d19cecf63327c"
tags: [perplexity, research, web-search, citations, synthesis]
---
# Perplexity AI for Research

## Summary

**One-sentence:** A workflow for using Perplexity Pro Search to synthesize cited multi-source research answers.

**One-paragraph:** A workflow for using Perplexity Pro Search to synthesize cited multi-source research answers. Sonnet decomposes a research question into atomic sub-queries; Haiku executes each Pro Search call; Sonnet synthesizes results and flags conflicting or low-confidence claims. Human reviews flagged items before findings enter any downstream pipeline.

## Applies If (ALL must hold)

- Fast synthesis of a research question requiring 5+ web sources simultaneously.
- Market sizing, competitive landscape, or trend research where citations matter.
- Fact-checking a specific claim with primary source validation.
- Generating a research brief or background document as a starting point for deeper analysis.
- When the question requires live web data (post-knowledge-cutoff events, current pricing, recent funding).

## Skip If (ANY kills it)

- When primary source documents (PDFs, internal databases) are required — Perplexity only searches the public web.
- For confidential competitive research — queries leak strategic intent via Perplexity's servers.
- When a single authoritative source is available directly — fetch it with a targeted HTTP call.
- For strategy or product decisions requiring reasoned tradeoffs — Perplexity retrieves, does not reason.

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
