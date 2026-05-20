---
slug: ai-design-assistant-patterns
tier: geek
group: ux
domain: ux-ui-designer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Methodology for selecting and specifying AI assistant interaction patterns within design tools: sidebar (persistent, long tasks), modal (single-shot high-stakes generation), and inline (micro-suggestions on selection).
content_id: "8ca2a4fd707493f8"
tags: [ai-ux, interaction-patterns, design-tools, human-ai-collaboration, assistant-ui]
---
# AI Design Assistant Patterns

## Summary

**One-sentence:** Methodology for selecting and specifying AI assistant interaction patterns within design tools: sidebar (persistent, long tasks), modal (single-shot high-stakes generation), and inline (micro-suggestions on selection).

**One-paragraph:** Methodology for selecting and specifying AI assistant interaction patterns within design tools: sidebar (persistent, long tasks), modal (single-shot high-stakes generation), and inline (micro-suggestions on selection). Covers trigger conditions, response formats, fallback states, human confirmation requirements, and anti-patterns that erode trust.

## Applies If (ALL must hold)

- Defining how an AI assistant should surface inside a design tool for a product feature
- Auditing an existing AI assistant UX for interaction pattern anti-patterns
- Generating design specifications for contextual, generative, or review-type AI assistants
- Selecting which assistant pattern (sidebar / modal / inline) fits a given task complexity

## Skip If (ANY kills it)

- When the AI capability itself is undefined — choose capability first, then interaction pattern
- Fully automated pipelines where no human interaction is expected during the AI task
- Mobile-first interfaces with minimal screen real estate where persistent sidebar degrades UX
- Purely mechanical tasks needing no conversational affordance (batch export, resize)

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
