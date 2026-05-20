---
slug: multimodal-vui-design
tier: geek
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design methodology for interfaces that combine voice input with visual display — pattern-matching voice commands to on-screen card/carousel output while maintaining touch fallbacks for every voice state.
content_id: "50c32b1c6dd76625"
tags: [voice-ui, multimodal, smart-display, accessibility, dialogue-design]
---
# Multimodal VUI Design

## Summary

**One-sentence:** Design methodology for interfaces that combine voice input with visual display — pattern-matching voice commands to on-screen card/carousel output while maintaining touch fallbacks for every voice state.

**One-paragraph:** Design methodology for interfaces that combine voice input with visual display — pattern-matching voice commands to on-screen card/carousel output while maintaining touch fallbacks for every voice state. Every dialogue turn must declare: voice prompt, visual state (max 5 items), valid touch actions, and silence fallback.

## Applies If (ALL must hold)

- Smart TV, smart display, kiosk, or automotive HMI combining voice with a screen
- Voice assistants surfacing structured data (product cards, search results, maps)
- Accessibility-first products where users alternate between touch and voice
- Conversational commerce (search → carousel → voice-confirm purchase)

## Skip If (ANY kills it)

- Audio-only environments (earbuds, phone IVR) — no screen; use pure VUI
- Text-heavy B2B tools (dashboards, IDEs) — voice adds friction with no multimodal benefit
- Products where latency >2s is unacceptable — ASR + LLM + TTS chain is inherently slow
- Teams without dedicated voice UX expertise — multimodal amplifies design errors

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

- parent skill: `geek/ux/ux-ui-designer/`
