---
slug: vui-market-context
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Voice assistants are used by 8.
content_id: "096c3178949f927c"
tags: [voice-ui, market-research, platforms, adoption, voice-trends]
---
# VUI Market Context

## Summary

**One-sentence:** Voice assistants are used by 8.

**One-paragraph:** Voice assistants are used by 8.4+ billion people globally; 62% of US adults use voice assistants; 71% prefer voice over typing. Five major platforms dominate (Alexa, Google Assistant, Siri, Bixby, custom LLM), but developer access is increasingly restricted except for Matter, Home Assistant, and custom LLM voice (Realtime API, Gemini Live, Pipecat).

## Applies If (ALL must hold)

- Drafting a "voice strategy" section in a product spec or investor pitch deck.
- Picking a target voice platform (Alexa vs. Google Assistant vs. open ecosystem vs. custom LLM) for an MVP.
- Writing competitive landscape or TAM slides for a voice-feature business case.
- Briefing a new hire on the voice ecosystem and developer access status before they design or build.

## Skip If (ANY kills it)

- Hands-on dialogue or interaction design — see core VUI design principles and conversation design methodologies instead.
- Privacy and security architecture — see the VUI privacy and security methodology.
- Pure technical evaluation of ASR/NLU vendors — use benchmark data and vendor comparisons, not market positioning.

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

- parent skill: `pro/ux/ux-ui-designer/`
