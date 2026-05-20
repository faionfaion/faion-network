---
slug: core-vui-design-principles
tier: pro
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Three testable principles for voice user interface design: (1) Simplicity — one idea per turn, no redundant phrasing; (2) Natural conversation — sound human, offer one helpful follow-up; (3) Context awareness — use prior turns implicitly, never restate what the user just said.
content_id: "f4ee38008ea70c40"
tags: [voice-ui, conversation-design, vui-principles, llm-output, dialog-design]
---
# Core VUI Design Principles

## Summary

**One-sentence:** Three testable principles for voice user interface design: (1) Simplicity — one idea per turn, no redundant phrasing; (2) Natural conversation — sound human, offer one helpful follow-up; (3) Context awareness — use prior turns implicitly, never restate what the user just said.

**One-paragraph:** Three testable principles for voice user interface design: (1) Simplicity — one idea per turn, no redundant phrasing; (2) Natural conversation — sound human, offer one helpful follow-up; (3) Context awareness — use prior turns implicitly, never restate what the user just said. Voice interfaces fail when designed like visual interfaces: dense information, no follow-up offers, and ignoring conversation history all break the spoken medium.

## Applies If (ALL must hold)

- Designing voice-first features (Alexa/Google Assistant skills, IVR, in-car voice, accessibility voice nav).
- Adding spoken output to multimodal agents where the LLM both listens and speaks.
- Auditing existing voice flows for verbosity, missing context tracking, or unnatural phrasing.
- Generating TTS-layer prompt/response copy where SSML, pacing, and turn-taking matter.

## Skip If (ANY kills it)

- Pure GUI/keyboard apps where voice is not a modality.
- Backend-only agents with no spoken output (text-chat agents need conversation design, not VUI principles).
- One-shot transactional bots where users never have a follow-up turn — those need scripts, not principles.

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
