---
slug: ai-design-assistant-patterns
tier: geek
group: ux
domain: ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Four interaction patterns for embedding AI assistance into design tools: sidebar (always-on contextual suggestions), modal (focused batch generation), inline (micro-corrections on selected elements), and review (audit passes against a structured rubric).
content_id: "8ca2a4fd707493f8"
tags: [design-systems, ai-assisted-design, figma-plugins, ux-patterns, agent-design]
---
# AI Design Assistant Patterns

## Summary

**One-sentence:** Four interaction patterns for embedding AI assistance into design tools: sidebar (always-on contextual suggestions), modal (focused batch generation), inline (micro-corrections on selected elements), and review (audit passes against a structured rubric).

**One-paragraph:** Four interaction patterns for embedding AI assistance into design tools: sidebar (always-on contextual suggestions), modal (focused batch generation), inline (micro-corrections on selected elements), and review (audit passes against a structured rubric). Choose one pattern per tool — mixing them creates UX confusion. Review-mode is the most agent-native: the agent receives a design artifact, applies a rubric, and returns structured JSON feedback for a human to act on.

## Applies If (ALL must hold)

- Implementing a contextual AI assistant inside a Figma plugin where the assistant reacts to selected/edited content
- Building a review-mode assistant that audits a design artifact and returns structured feedback
- Automating design documentation: converting Figma JSON or component specs into human-readable specs
- Evaluating which interaction pattern fits a given tool's UX before committing to implementation

## Skip If (ANY kills it)

- The design problem is novel or strategic — assistant patterns support execution, not vision-setting
- The assistant would make irreversible changes autonomously — all AI design actions must be reversible or human-confirmed
- Context window is insufficient for the full design artifact (Figma file JSON above 200k tokens) — the assistant will hallucinate missing details
- The user base has low AI literacy — assistant patterns require users to interpret and validate output

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
