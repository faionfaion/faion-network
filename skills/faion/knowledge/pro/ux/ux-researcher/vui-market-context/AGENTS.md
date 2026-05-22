---
slug: vui-market-context
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Voice market context: adoption stats and platform comparison for strategic decision-making.
content_id: "096c3178949f927c"
tags: [voice-market, platform-comparison, market-research, adoption-stats, strategy]
---
# VUI Market Context

## Summary

**One-sentence:** Voice market context: adoption stats and platform comparison for strategic decision-making.

**One-paragraph:** Voice market context: adoption stats and platform comparison for strategic decision-making.

## Applies If (ALL must hold)

- Strategy phase of a voice-product proposal: ground the deck in current adoption stats and platform tradeoffs.
- Platform-selection decision: choose Alexa vs Google Assistant vs Siri vs custom LLM-VUI based on developer surface and user reach in target geos.
- Quarterly brief refresh: market data ages fast; agents pull current numbers on demand instead of relying on stale README values.
- Investor / stakeholder primers: a one-page market context written from canonical sources (Statista, Voicebot.ai, NNg, Gartner).

## Skip If (ANY kills it)

- Implementation work — this methodology is descriptive market context, not how-to.
- Single-vendor decisions already locked — re-justification is not useful.
- Real-time competitive intelligence — use a market-research methodology with monitoring loops instead.

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

- parent skill: `pro/ux/ux-researcher/`
