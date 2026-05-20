---
slug: multimodal-vui-design
tier: geek
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design voice + visual interfaces for smart displays by specifying four interaction patterns (voice-initiated screen-completed, screen-initiated voice-completed, voice + visual feedback, voice navigation + visual content) and enforcing a three-tier fallback hierarchy (voice → touch → keyboard).
content_id: "50c32b1c6dd76625"
tags: [multimodal, voice-ui, smart-display, apl, fallback]
---
# Multimodal VUI Design

## Summary

**One-sentence:** Design voice + visual interfaces for smart displays by specifying four interaction patterns (voice-initiated screen-completed, screen-initiated voice-completed, voice + visual feedback, voice navigation + visual content) and enforcing a three-tier fallback hierarchy (voice → touch → keyboard).

**One-paragraph:** Design voice + visual interfaces for smart displays by specifying four interaction patterns (voice-initiated screen-completed, screen-initiated voice-completed, voice + visual feedback, voice navigation + visual content) and enforcing a three-tier fallback hierarchy (voice → touch → keyboard). Every feature requires explicit timeout behavior, error state handling, and state-sync verification.

## Applies If (ALL must hold)

- Designing a voice interface for a smart display (Amazon Echo Show, Google Nest Hub, Alexa TV)
- Building a product combining voice input with screen output
- Auditing an existing VUI for missing visual fallbacks
- Generating APL or equivalent smart display template markup from a design brief
- Prototyping a multimodal conversation flow where visual selection resolves voice ambiguity

## Skip If (ANY kills it)

- Building a voice-only screenless speaker interface — pure VUI methodology is more appropriate
- Building a screen-only UI with optional voice layer — voice-initiated patterns add no value
- Target device has no reliable microphone (high-noise kiosk without directional mic)
- User research shows the target audience strongly opposes voice interaction

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

- parent skill: `geek/ux/ui-designer/`
