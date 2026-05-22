---
slug: voice-ui-patterns
tier: pro
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Practical patterns for designing voice user interfaces: prompt writing rules, progressive error recovery (3-step ladder), multimodal voice+screen coordination, platform-specific constraints (Alexa, Google Actions, Siri), and key performance metrics.
content_id: "9f49dd3015fc354d"
tags: [voice-ui, vui, conversation-design, voice-agents]
---
# Voice UI Patterns

## Summary

**One-sentence:** Practical patterns for designing voice user interfaces: prompt writing rules, progressive error recovery (3-step ladder), multimodal voice+screen coordination, platform-specific constraints (Alexa, Google Actions, Siri), and key performance metrics.

**One-paragraph:** Practical patterns for designing voice user interfaces: prompt writing rules, progressive error recovery (3-step ladder), multimodal voice+screen coordination, platform-specific constraints (Alexa, Google Actions, Siri), and key performance metrics. The core discipline is designing for the ear, not the eye — one idea per turn, concise confirmations only for high-stakes actions, and always providing an escape hatch.

## Applies If (ALL must hold)

- Designing a new voice skill (Alexa, Google Action, Siri Shortcut, or custom voice bot).
- Producing prompt copy, error ladders, and confirmation patterns from a feature spec.
- Auditing an existing voice flow against NNG / Google / Amazon design guidelines.
- Designing multimodal (voice + screen) flows for display devices.

## Skip If (ANY kills it)

- Pure text chatbots with no audio — use chatbot conversation-design playbooks instead.
- IVR with regulatory script requirements (banking, healthcare) — legal-mandated wording overrides UX guidance.
- Pre-product validation phase — design utterances on real user data, not imagined scripts.
- Languages with limited TTS quality where prosody coaching is futile.

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

- parent skill: `pro/ux/ui-designer/`
