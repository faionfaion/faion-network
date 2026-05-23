---
slug: vui-market-context
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a one-page voice market brief with sourced adoption stats + platform comparison weighted by target geo.
content_id: "096c3178949f927c"
complexity: medium
produces: report
est_tokens: 4400
tags: [voice-market, platform-comparison, market-research, adoption-stats, strategy]
---
# VUI Market Context

## Summary

**One-sentence:** Generates a one-page voice market brief with sourced adoption stats + platform comparison weighted by target geo.

**One-paragraph:** Voice market context grounds a platform-selection or stakeholder pitch in concrete, sourced figures rather than anecdote. Every statistic carries value + year + source URL + geographic scope; briefs older than 90 days are refused. Five platforms in scope: Alexa, Google Assistant, Siri, Bixby, custom LLM-VUI (treated as a distinct fifth category, not a feature). Refresh runs via Anthropic web_search against an explicit trusted-source allowlist (Statista, Voicebot.ai, Edison/Infinite Dial, NN/g, Pew, Gartner). Output is a markdown brief plus a JSON metric snapshot fit for re-use.

**Ефективно для:**

- Платформне рішення (Alexa vs Google vs Siri vs LLM-native) для voice-продукту на 2-річний горизонт.
- Quarterly refresh короткої довідки для stakeholder/investor deck — без застарілих цифр.
- Pitch до інвестора з обґрунтованими adoption-статистиками + scope per geo.
- Платформний trade-off-аналіз з акцентом на target geo, а не глобальну частку.

## Applies If (ALL must hold)

- Strategy phase of a voice-product proposal: ground the deck in current adoption stats and platform tradeoffs.
- Platform-selection decision: Alexa vs Google Assistant vs Siri vs custom LLM-VUI by developer surface and user reach in target geos.
- Quarterly brief refresh: market data ages fast — agents pull current numbers on demand instead of relying on stale README values.

## Skip If (ANY kills it)

- Implementation work — this methodology is descriptive market context, not how-to.
- Single-vendor decisions already locked — re-justification is not useful.
- Real-time competitive intelligence — use a market-research methodology with monitoring loops instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Target geos list | YAML list of ISO country codes | product brief |
| Trusted source allowlist | text list | this methodology |
| ANTHROPIC_API_KEY | env var | provider account |
| Metric list | text list of ≥4 metrics | this methodology default |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[market-researcher]] | Upstream — supplies general market-data normalization rules |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: scoped-stat-fields, denominator-discipline, 90-day-freshness, trusted-source-allowlist, llm-native-as-platform | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for brief + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: hallucinated-stats, mixed-denominators, geo-scope-confusion, stale-brief | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure: collect → refresh → normalize → assemble → publish | 800 |
| `content/05-examples.xml` | essential | Worked brief example for a US+EU smart-speaker product | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree: brief age + scope completeness → action | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `refresh-metrics-from-web` | sonnet | Web search + JSON normalization, mechanical. |
| `assemble-brief-narrative` | sonnet | Light judgment composing per-geo narrative. |
| `validate-brief-schema` | haiku | Schema check is deterministic. |

## Templates

| File | Purpose |
|------|---------|
| `templates/refresh-script.py` | Anthropic web_search refresh runner emitting `vui_market_brief.json` |
| `templates/brief.md` | Markdown brief skeleton with stats + platform comparison sections |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vui-market-context.py` | Validate `vui_market_brief.json` against the output schema | Pre-commit / CI on every refresh |

## Related

- [[market-researcher]]
- [[vui-conversation-design]]
- [[core-vui-design-principles]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes from observable inputs (brief age, presence of geo scope, denominator type) to an action, each leaf referencing a rule from `01-core-rules.xml`. Use it when deciding whether to publish, refresh, or reject a candidate stat.
