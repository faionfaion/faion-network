---
slug: vui-market-context
tier: pro
group: ux
domain: ux
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a voice-platform decision record comparing the five major voice platforms (Alexa, Google Assistant, Siri, Bixby, custom LLM) on developer access, install base, distribution, and Matter / Home Assistant openness as of 2026.
content_id: "096c3178949f927c"
complexity: medium
produces: decision-record
est_tokens: 4000
tags: [voice-ui, market-research, platforms, adoption, voice-trends]
---
# VUI Market Context

## Summary

**One-sentence:** Produces a voice-platform decision record comparing the five major voice platforms (Alexa, Google Assistant, Siri, Bixby, custom LLM) on developer access, install base, distribution, and Matter / Home Assistant openness as of 2026.

**One-paragraph:** Voice assistants reach billions of users, but developer access to the major platforms is increasingly restricted. Alexa Skills, Google Actions, and SiriKit are partial. Open paths remain via Matter (smart home), Home Assistant (self-hosted), and custom LLM voice (OpenAI Realtime API, Gemini Live, Pipecat). This methodology produces a voice-platform decision record citing 2025-2026 install base + developer access + distribution constraints, with primary + fallback channels and an explicit lock-in risk note.

**Ефективно для:**

- Pre-funding choice of voice platform (which assistants to ship on first).
- Cross-platform reach analysis (Alexa + Google + custom-LLM).
- Smart-home product platform decision (Matter vs Home Assistant vs vendor walled garden).
- Lock-in risk assessment for voice products dependent on a single platform.

## Applies If (ALL must hold)

- Product targets consumer voice assistants OR custom LLM voice.
- Funding / steering decision still open.
- GTM strategy depends on platform install base + developer access.

## Skip If (ANY kills it)

- Internal-only voice prototype — no platform decision needed.
- Custom-LLM-only product where vendor platforms are already excluded.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Use-case description | Markdown | PM |
| Audience profile | persona doc | research |
| Distribution channel preferences | list | GTM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | self-contained methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: cite-2025-2026-data, score-developer-access, primary-plus-fallback, matter-or-ha-for-smart-home, custom-llm-voice-allowed | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the produced artefact + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 900 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals -> rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify-use-case` | haiku | Enum pick. |
| `pull-data` | sonnet | Source citation + freshness check. |
| `score-platforms` | sonnet | Multi-criteria reasoning. |
| `red-team` | opus | Adversarial review. |

## Templates

| File | Purpose |
|------|---------|
| `templates/decision-record.md` | Skeleton voice-platform decision record |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-vui-market-context.py` | Validate the artefact against the schema | Pre-commit; CI on each artefact change |

## Related

- [[voice-ui]]
- [[vui-iot-integration]]
- [[vui-conversation-design]]

## Decision tree

See `content/06-decision-tree.xml`. Branches by use-case → platform recommendation. Smart-home routes through Matter / Home Assistant requirement. Each leaf cites a rule from `01-core-rules.xml`.
